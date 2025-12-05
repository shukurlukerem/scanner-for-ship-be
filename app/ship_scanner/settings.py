"""
Django settings for ship_scanner project.
"""

from pathlib import Path
import environ
import os

# ==========================================
#               ENV SETTINGS
# ==========================================
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY", default="dev-secret-key")
DEBUG = env("DEBUG", default=True)

ALLOWED_HOSTS = [
    "*",
    "46.224.67.166",
    "localhost",
]

# ==========================================
#              INSTALLED APPS
# ==========================================
INSTALLED_APPS = [
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "scanner",

    "rest_framework",
    "drf_spectacular",
    "corsheaders",
]

# ==========================================
#               MIDDLEWARE
# ==========================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ship_scanner.urls"

# ==========================================
#             REST FRAMEWORK
# ==========================================
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "scanner.authentication.ScannerTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# ==========================================
#                TEMPLATES
# ==========================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ship_scanner.wsgi.application"

# ==========================================
#                 DATABASE
# ==========================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

# ==========================================
#         PASSWORD VALIDATION
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

# ==========================================
#               LOCALIZATION
# ==========================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Khartoum"
USE_I18N = True
USE_TZ = True

# ==========================================
#               STATIC FILES
# ==========================================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = []

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==========================================
#             JAZZMIN SETTINGS
# ==========================================
JAZZMIN_SETTINGS = {
    "site_title": "Ship Scanner Admin",
    "site_header": "Ship Scanner",
    "site_brand": "Ship Scanner",
    "welcome_sign": "Welcome to Ship Scanner Admin Panel",

    "custom_links": {
        "scanner": [
            {
                "name": "Scanner Page",
                "url": "/scan/",
                "icon": "fas fa-qrcode",
            }
        ]
    },

    "icons": {"scanner.ScanLog": "fas fa-history"},
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly"
}

# ==========================================
#                CORS / CSRF
# ==========================================

CORS_ALLOW_ALL_ORIGINS = False   # təhlükəsiz & dəqiq

CORS_ALLOWED_ORIGINS = [
    "http://46.224.67.166:8010",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]


# header-lər
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-requested-with",
    "ngrok-skip-browser-warning",
]

# metodlar
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_CREDENTIALS = True
CORS_PREFLIGHT_MAX_AGE = 86400

# bu çox vacibdir – CSRF errorlarının 90%-ni həll edir
CSRF_TRUSTED_ORIGINS = [
    "http://46.224.67.166:8010",
    "http://46.224.67.166",
    "https://46.224.67.166",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]


# ==========================================
#           PROXY / SSL HEADERS
# ==========================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

