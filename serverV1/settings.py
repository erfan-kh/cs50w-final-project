# Import required modules
from pathlib import Path
import os

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pf@(lg!dm&*r3g5#gm0tq+ib9inr!1wpqwy+7ijrqp_^0q*z#r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# List of hosts allowed to connect to this Django application
ALLOWED_HOSTS = ["192.168.1.100", "127.0.0.1",
                 "localhost", "fly-sharp-extremely.ngrok-free.app"]

# Set the X-Frame-Options header used by Django SecurityMiddleware
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_CROSS_ORIGIN_OPENER_POLICY = "None"
# List of trusted origins for CSRF
CSRF_TRUSTED_ORIGINS = ["https://fly-sharp-extremely.ngrok-free.app"]

# List of applications installed in this Django project
INSTALLED_APPS = [
    'serverv',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# List of middleware classes used by this Django project
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# The URL configuration module for the project
ROOT_URLCONF = 'serverV1.urls'

# Configuration for Django templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application used by Django's runserver
WSGI_APPLICATION = 'serverV1.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Custom user model
AUTH_USER_MODEL = "serverv.User"

# Password validation rules
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Language code for this installation
LANGUAGE_CODE = 'en-us'

# Time zone for this installation
TIME_ZONE = 'Asia/Tehran'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
STATIC_URL = 'static/'

# The default auto field type to use for auto-created primary keys.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
