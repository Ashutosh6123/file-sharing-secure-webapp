from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from files.models import UploadedFile
from django.urls import reverse
from django.contrib import messages
from django.db import models
from .forms import OpsUserRegistrationForm, ClientUserRegistrationForm
from .utils import send_magic_login_email, validate_magic_token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import ClientSignupSerializer, LoginSerializer
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import URLSafeTimedSerializer
from rest_framework.authtoken.models import Token

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

# -----------------------------
# ✅ API Views
# -----------------------------
class ClientSignupView(APIView):
    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = serializer.dumps(user.email, salt='email-verify')
            link = f"http://localhost:8000/api/verify-email/{token}/"
            send_mail(
                subject="Verify your email",
                message=f"Click here to verify your email: {link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email]
            )
            return Response({"message": "Verification email sent", "verification_link": link})
        return Response(serializer.errors, status=400)

class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            email = serializer.loads(token, salt='email-verify', max_age=3600)
            user = CustomUser.objects.get(email=email)
            user.is_active = True
            user.email_verified = True
            user.save()
            return Response({"message": "Email verified successfully"})
        except CustomUser.DoesNotExist:
            return Response({"error": "No user found for email"}, status=404)
        except Exception as e:
            return Response({"error": "Invalid or expired token"}, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status=400)

# -----------------------------
# ✅ Web Views (Template-based)
# -----------------------------

def home(request):
    """Home page with navigation options"""
    return render(request, 'home.html')

def ops_register(request):
    """Registration form for operations users"""
    if request.method == 'POST':
        form = OpsUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Operations account created successfully! You can now login.')
            return redirect('login')
    else:
        form = OpsUserRegistrationForm()
    return render(request, 'register_ops.html', {'form': form})

def client_register(request):
    """Registration form for client users"""
    if request.method == 'POST':
        form = ClientUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Client account created successfully! You can now login.')
            return redirect('login')
    else:
        form = ClientUserRegistrationForm()
    return render(request, 'register_client.html', {'form': form})

def user_login(request):
    """General login view - Verification link only"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'login.html')
        
        try:
            # Find user by email (both ops and client users)
            user = CustomUser.objects.filter(
                email=email, 
                is_active=True
            ).filter(
                models.Q(is_client=True) | models.Q(is_ops=True)
            ).first()
            
            if user:
                success, message = send_magic_login_email(user, request)
                
                if success:
                    messages.success(request, f'Verification login link sent to {email}. Please check your email.')
                else:
                    messages.error(request, f'Failed to send email: {message}')
            else:
                # Don't reveal if email exists or not for security
                messages.info(request, f'If {email} is registered as a user, a verification login link has been sent.')
                
        except Exception:
            # Don't reveal if email exists or not for security
            messages.info(request, f'If {email} is registered as a user, a verification login link has been sent.')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_ops(request):
    if not request.user.is_ops:
        return redirect('login')
    
    if request.method == 'POST' and request.FILES.get('file'):
        f = request.FILES['file']
        if f.name.endswith(('.docx', '.pptx', '.xlsx')):
            UploadedFile.objects.create(uploader=request.user, file=f)

    files = UploadedFile.objects.all()
    return render(request, 'dashboard_ops.html', {'files': files})

@login_required
def dashboard_client(request):
    if not request.user.is_client:
        return redirect('login')
    
    files = UploadedFile.objects.all()
    return render(request, 'dashboard_client.html', {'files': files})

def ops_login(request):
    """Login view specifically for operations users - Verification link only"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'login_ops.html')
        
        try:
            # Find operations user by email
            user = CustomUser.objects.filter(
                email=email, 
                is_active=True,
                is_ops=True
            ).first()
            
            if user:
                success, message = send_magic_login_email(user, request)
                
                if success:
                    messages.success(request, f'Verification login link sent to {email}. Please check your email.')
                else:
                    messages.error(request, f'Failed to send email: {message}')
            else:
                # Don't reveal if email exists or not for security
                messages.info(request, f'If {email} is registered as an operations user, a verification login link has been sent.')
                
        except Exception:
            # Don't reveal if email exists or not for security
            messages.info(request, f'If {email} is registered as an operations user, a verification login link has been sent.')
    
    return render(request, 'login_ops.html')

def client_login(request):
    """Login view specifically for client users - Verification link only"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'login_client.html')
        
        try:
            # Find client user by email
            user = CustomUser.objects.filter(
                email=email, 
                is_active=True,
                is_client=True
            ).first()
            
            if user:
                success, message = send_magic_login_email(user, request)
                
                if success:
                    messages.success(request, f'Verification login link sent to {email}. Please check your email.')
                else:
                    messages.error(request, f'Failed to send email: {message}')
            else:
                # Don't reveal if email exists or not for security
                messages.info(request, f'If {email} is registered as a client user, a verification login link has been sent.')
                
        except Exception:
            # Don't reveal if email exists or not for security
            messages.info(request, f'If {email} is registered as a client user, a verification login link has been sent.')
    
    return render(request, 'login_client.html')

def magic_login(request, token):
    """Handle verification login from email link"""
    magic_token, error = validate_magic_token(token)
    
    if error:
        messages.error(request, error)
        return redirect('home')
    
    if magic_token:
        # Mark token as used
        magic_token.is_used = True
        magic_token.save()
        
        # Log the user in
        login(request, magic_token.user)
        messages.success(request, f'Welcome back, {magic_token.user.get_full_name() or magic_token.user.username}! You have been automatically logged in.')
        
        # Redirect to appropriate dashboard based on user type
        if magic_token.user.is_ops:
            return redirect('dashboard_ops')
        elif magic_token.user.is_client:
            return redirect('dashboard_client')
        else:
            return redirect('home')
    
    messages.error(request, 'Invalid verification link.')
    return redirect('home')

def request_magic_login(request):
    """Allow users to request a verification login link via email"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'request_magic_login.html')
        
        try:
            # Support both ops and client users
            user = CustomUser.objects.filter(
                email=email, 
                is_active=True
            ).filter(
                models.Q(is_client=True) | models.Q(is_ops=True)
            ).first()
            
            if user:
                success, message = send_magic_login_email(user, request)
                
                if success:
                    messages.success(request, f'Verification login link sent to {email}. Please check your email.')
                else:
                    messages.error(request, f'Failed to send email: {message}')
            else:
                # Don't reveal if email exists or not for security
                messages.info(request, f'If {email} is registered as a user, a verification login link has been sent.')
                
        except Exception:
            # Don't reveal if email exists or not for security
            messages.info(request, f'If {email} is registered as a user, a verification login link has been sent.')
    
    return render(request, 'request_magic_login.html')
