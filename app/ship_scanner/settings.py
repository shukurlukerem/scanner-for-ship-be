"""
Django settings for ship_scanner project.
"""

from pathlib import Path
import environ
import os

# ============================
#       ENV SETTINGS
# ============================
env = environ.Env(DEBUG=(bool, False))
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY", default="dev-secret-key")
DEBUG = env("DEBUG")

# Parse ALLOWED_HOSTS from env OR use defaults
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
        "38.242.145.252",
        ".ngrok-free.app",
        ".ngrok.app",
        ".ngrok.io",
        "*",    # Son çarə — ngrok üçün
    ]
)

# =======================
#     INSTALLED APPS
# =======================
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps
    "scanner",

    # API
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",

    # CORS
    "corsheaders",
]

# =======================
#       MIDDLEWARE
# =======================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "corsheaders.middleware.CorsMiddleware",   # CORS always first (after security)

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "ship_scanner.urls"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# =======================
#         TEMPLATES
# =======================
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

# =======================
#        DATABASE
# =======================
DATABASES = {
    "default": env.db(),
}

# =======================
#   PASSWORD VALIDATION
# =======================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =======================
#     INTERNATIONAL
# =======================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =======================
#     STATIC FILES
# =======================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = []


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ====================================================
#                JAZZMIN SETTINGS
# ====================================================
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
                "permissions": ["auth.view_user"],
            },
        ]
    },

    "icons": {
        "scanner.ScanLog": "fas fa-history",
    },

    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": None,
}

# ====================================================
#              CORS + CSRF SETTINGS
# ====================================================

# CORS allowed
CORS_ALLOW_ALL_ORIGINS = True   # Ngrok + Local + IP üçün lazımdır

CORS_ALLOW_CREDENTIALS = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    "http://38.242.145.252",
    "https://38.242.145.252",

    "https://*.ngrok-free.app",
    "https://*.ngrok.app",
    "https://*.ngrok.io",
]

# Ngrok HTTPS fix
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookie security (HTTPS üçün)
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
