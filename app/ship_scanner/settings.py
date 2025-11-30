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

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
        "38.242.145.252",
        "kpsraufbey.site",
        "www.kpsraufbey.site",
        "*",
    ]
)

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

    "corsheaders.middleware.CorsMiddleware",   # MUST BE HERE
    "django.middleware.common.CommonMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ship_scanner.urls"

# ==========================================
#               REST FRAMEWORK
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
    "default": env.db(),
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
TIME_ZONE = "UTC"
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
#              JAZZMIN SETTINGS
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
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://kpsraufbey.site",
    "https://www.kpsraufbey.site",
    "http://kpsraufbey.site",
    "http://www.kpsraufbey.site",

    "http://38.242.145.252",
    "http://38.242.145.252:8010",
    "https://38.242.145.252",
    "https://38.242.145.252:8010",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_CREDENTIALS = True

CORS_PREFLIGHT_MAX_AGE = 86400


CSRF_TRUSTED_ORIGINS = [
    "https://kpsraufbey.site",
    "https://www.kpsraufbey.site",
    "http://kpsraufbey.site",
    "http://www.kpsraufbey.site",

    "http://38.242.145.252",
    "http://38.242.145.252:8010",
    "https://38.242.145.252",
    "https://38.242.145.252:8010",
]


# ==========================================
#     PROXY / SSL (ngrok / nginx)
# ==========================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
