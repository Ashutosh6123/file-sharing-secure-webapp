from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from files.models import UploadedFile
from django.urls import reverse
from django.contrib import messages
from .forms import OpsUserRegistrationForm, ClientUserRegistrationForm

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
    message = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if user.is_ops:
                return redirect('dashboard_ops')
            elif user.is_client:
                return redirect('dashboard_client')
        else:
            message = "Invalid username or password"
    return render(request, 'login.html', {'message': message})

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
    """Login view specifically for operations users"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_ops:
                login(request, user)
                return redirect('dashboard_ops')
            else:
                messages.error(request, 'This account is not authorized for operations access.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login_ops.html')

def client_login(request):
    """Login view specifically for client users"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_client:
                login(request, user)
                return redirect('dashboard_client')
            else:
                messages.error(request, 'This account is not authorized for client access.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login_client.html')
