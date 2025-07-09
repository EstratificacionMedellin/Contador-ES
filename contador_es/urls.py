from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from esapp.views import asignar, reporte, dashboard

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),

    # Autenticación de usuario
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Recuperación y restablecimiento de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Vistas personalizadas
    path('', asignar, name='asignar'),
    path('reporte/', reporte, name='reporte'),
    path('dashboard/', dashboard, name='dashboard'),

    # Rutas de autenticación por defecto de Django
    path('accounts/', include('django.contrib.auth.urls')),
]

# Archivos estáticos en entorno de desarrollo
if settings.DEBUG:
    static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
    if static_dirs:
        urlpatterns += static(settings.STATIC_URL, document_root=static_dirs[0])
