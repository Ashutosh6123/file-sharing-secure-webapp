from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .models import MagicLoginToken
from .email_utils import send_email_with_retry
import uuid

def get_client_ip(request):
    """Get the client's IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_agent(request):
    """Get the user agent from the request"""
    return request.META.get('HTTP_USER_AGENT', '')

def create_magic_login_token(user, request):
    """Create a magic login token for the user"""
    # Invalidate any existing unused tokens for this user
    MagicLoginToken.objects.filter(user=user, is_used=False).update(is_used=True)
    
    # Create new token
    token = MagicLoginToken.objects.create(
        user=user,
        token=str(uuid.uuid4()),
        login_ip=get_client_ip(request),
        user_agent=get_user_agent(request)
    )
    return token

def send_magic_login_email(user, request):
    """Send magic login email to the user"""
    # Allow verification login for both ops and client users
    if not (user.is_client or user.is_ops):
        return False, "Verification login is only available for registered users"
    
    try:
        # Create magic token
        magic_token = create_magic_login_token(user, request)
        
        # Build the verification link
        magic_link = request.build_absolute_uri(
            reverse('magic_login', kwargs={'token': magic_token.token})
        )
        
        # Prepare email context
        context = {
            'user': user,
            'magic_link': magic_link,
            'login_time': timezone.now().strftime('%B %d, %Y at %I:%M %p'),
            'user_ip': get_client_ip(request),
            'user_agent': get_user_agent(request),
        }
        
        # Render email templates
        html_message = render_to_string('emails/magic_login.html', context)
        plain_message = render_to_string('emails/magic_login.txt', context)
        
        # Send email with retry mechanism
        success, message = send_email_with_retry(
            subject='🔗 Your Verification Login Link - Secure File Share',
            message=plain_message,
            recipient_list=[user.email],
            html_message=html_message,
            max_retries=3
        )
        
        if success:
            return True, f"Verification login link sent to {user.email}"
        else:
            return False, message
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

def validate_magic_token(token_string):
    """Validate and return magic login token if valid"""
    try:
        token = MagicLoginToken.objects.get(token=token_string)
        if token.is_valid():
            return token, None
        else:
            error = "expired" if timezone.now() >= token.expires_at else "already used"
            return None, f"This verification link has {error}. Please request a new one."
    except MagicLoginToken.DoesNotExist:
        return None, "Invalid verification link. Please check the URL or request a new one."
