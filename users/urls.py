from django.urls import path
from .views import (
    user_login, user_logout, dashboard_ops, dashboard_client, 
    ClientSignupView, VerifyEmailView, LoginView,
    home, ops_register, client_register, ops_login, client_login, magic_login, request_magic_login
)

urlpatterns = [
    # Home and authentication
    path('', home, name='home'),
    path('login/', user_login, name='login'),  # General login (backward compatibility)
    path('ops-login/', ops_login, name='ops_login'),
    path('client-login/', client_login, name='client_login'),
    path('logout/', user_logout, name='logout'),
    
    # Magic login
    path('magic-login/<str:token>/', magic_login, name='magic_login'),
    path('request-magic-login/', request_magic_login, name='request_magic_login'),
    
    # Registration
    path('ops-register/', ops_register, name='ops_register'),
    path('client-register/', client_register, name='client_register'),
    
    # Dashboards
    path('dashboard-ops/', dashboard_ops, name='dashboard_ops'),
    path('dashboard-client/', dashboard_client, name='dashboard_client'),

    # API views
    path('api/signup/', ClientSignupView.as_view(), name='client_signup'),
    path('api/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('api/login/', LoginView.as_view(), name='api_login'),
]
