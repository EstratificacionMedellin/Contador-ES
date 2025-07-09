from decouple import config
from pathlib import Path

# 📁 Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Seguridad
SECRET_KEY = config('SECRET_KEY', default='inseguro-usar-en-desarrollo')
DEBUG = True
ALLOWED_HOSTS = ['10.125.8.148', 'localhost', '127.0.0.1']

# 📦 Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps externas
    'widget_tweaks',

    # Apps locales
    'esapp',
]

# 🧱 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 🔗 URLs principales
ROOT_URLCONF = 'contador_es.urls'

# 🧩 Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necesario para recuperación de contraseña
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🚀 WSGI
WSGI_APPLICATION = 'contador_es.wsgi.application'

# 🛢️ Bases de datos PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    },
    'secundaria': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME_DEV'),
        'USER': config('DB_USER_DEV'),
        'PASSWORD': config('DB_PASSWORD_DEV'),
        'HOST': config('DB_HOST_DEV'),
        'PORT': config('DB_PORT_DEV'),
        'OPTIONS': {
            'options': '-c search_path=catastro_alfa_sap,public'
        }
    }
}

# 🔐 Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Configuración regional
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# 🖼️ Archivos estáticos (CSS, JS, imágenes)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Aquí debes tener tus carpetas img, css, js
]

# ✅ Configuración para archivos subidos (opcional si usas uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🔐 Configuración de autenticación
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# 🛠️ Email para recuperación de contraseña (modo desarrollo)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 🆔 ID automático
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
