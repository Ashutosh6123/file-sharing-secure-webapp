from django.contrib import admin
from django.urls import path, include
from users.views import user_login, user_logout, dashboard_ops, dashboard_client, home
from files.views import generate_secure_link

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home page
    path('', home, name='home'),

    # Authentication (backward compatibility)
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard-ops/', dashboard_ops, name='dashboard_ops'),
    path('dashboard-client/', dashboard_client, name='dashboard_client'),
    path('generate-link/<int:file_id>/', generate_secure_link, name='generate_link'),

    # Include app URLs
    path('', include('users.urls')),
    path('api/', include('files.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
