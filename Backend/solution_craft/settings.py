import pymysql
pymysql.install_as_MySQLdb()

import os
from pathlib import Path
from datetime import timedelta

# Secret key for security (use environment variable for production)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-secret-key')

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Debug mode
DEBUG = True

# Allowed hosts for the application
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Security settings
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# JWT authentication settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Set the token expiration time
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Set the refresh token expiration time
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

# Installed applications
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',       
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'solution_craft_app',         
]

# Middleware configuration
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Custom user model setting
AUTH_USER_MODEL = 'solution_craft_app.CustomUser'

# Root URL configuration
ROOT_URLCONF = 'solution_craft.urls'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'solution_craft_db',
        'USER': 'root',
        'PASSWORD': 'Liltretre123!',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # BASE_DIR / 'solution_craft_app' / 'templates'
        ],
        'APP_DIRS': True,  # Enable automatic template loading from each app's templates folder
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

# CORS settings for frontend API access
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",  # Frontend running at this address
    "http://localhost:5500",   # Frontend running at this address
]

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Static files settings
STATIC_URL = '/static/'

# Static files directories
STATICFILES_DIRS = [
    BASE_DIR / "solution_craft_app" / "static",  
]

# Media files settings (if any)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
