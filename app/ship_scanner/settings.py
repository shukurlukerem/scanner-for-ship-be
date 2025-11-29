# """
# Django settings for ship_scanner project.
# """

# from pathlib import Path
# import environ
# import os

# env = environ.Env(DEBUG=(bool, False))

# # BASE DIR
# BASE_DIR = Path(__file__).resolve().parent.parent
# environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# # SECURITY
# SECRET_KEY = 'django-insecure-ki035yd3jlo9d3#3z*rl5bm2=qh)i2^rtug2%kj1$+hja*#%vz'
# DEBUG = True
# ALLOWED_HOSTS = ["*"]


# # =======================
# #     INSTALLED APPS
# # =======================
# INSTALLED_APPS = [
#     "jazzmin",                      # Jazzmin must be first
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "scanner"
# ]

# # =======================
# #       MIDDLEWARE
# # =======================
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "ship_scanner.urls"


# # =======================
# #         TEMPLATES
# # =======================
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]


# WSGI_APPLICATION = "ship_scanner.wsgi.application"


# # =======================
# #        DATABASE
# # =======================
# DATABASES = {
#     "default": env.db(),
# }


# # =======================
# #   PASSWORD VALIDATION
# # =======================
# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]


# # =======================
# #     INTERNATIONAL
# # =======================
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "UTC"
# USE_I18N = True
# USE_TZ = True


# # =======================
# #     STATIC FILES FIXED
# # =======================
# STATIC_URL = "/static/"

# # Static files collected here (Docker volume)
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# # DO NOT include non-existing static folders
# STATICFILES_DIRS = []


# # =======================
# #       DEFAULT PK
# # =======================
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# # ====================================================
# #                 JAZZMIN SETTINGS
# # ====================================================
# JAZZMIN_SETTINGS = {
#     "site_title": "Ship Scanner Admin",
#     "site_header": "Ship Scanner",
#     "site_brand": "Ship Scanner",
#     "welcome_sign": "Welcome to Ship Scanner Admin Panel",

#     "custom_links": {
#         "scanner": [
#             {
#                 "name": "Scanner Page",
#                 "url": "/scan/",
#                 "icon": "fas fa-qrcode",
#                 "permissions": ["auth.view_user"],
#             },
#         ]
#     },

#     # Scanner app-in öz modeli sidebar-a düşəcək
#     "icons": {
#         "scanner.ScanLog": "fas fa-history",
#     },

#     "show_ui_builder": False,
# }




# JAZZMIN_UI_TWEAKS = {
#     "theme": "flatly",
#     "dark_mode_theme": None,
#     "navbar_small_text": False,
#     "footer_small_text": False,
#     "body_small_text": False,
#     "brand_small_text": False,
#     "button_classes": {
#         "primary": "btn-primary",
#         "secondary": "btn-secondary",
#         "info": "btn-info",
#         "warning": "btn-warning",
#         "danger": "btn-danger",
#         "success": "btn-success",
#     },
# }

"""
Django settings for ship_scanner project.
"""

from pathlib import Path
import environ
import os

env = environ.Env(DEBUG=(bool, False))

# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY
SECRET_KEY = 'django-insecure-ki035yd3jlo9d3#3z*rl5bm2=qh)i2^rtug2%kj1$+hja*#%vz'
DEBUG = True

# Ngrok üçün geniş icazələr
ALLOWED_HOSTS = ["*", ".ngrok-free.app", ".ngrok.app", ".ngrok.io"]


# =======================
#     INSTALLED APPS
# =======================
INSTALLED_APPS = [
    "jazzmin",                      # Jazzmin must be first
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "scanner",
]

# =======================
#       MIDDLEWARE
# =======================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ship_scanner.urls"


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
#     STATIC FILES FIXED
# =======================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = []


# =======================
#       DEFAULT PK
# =======================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ====================================================
#                 JAZZMIN SETTINGS
# ====================================================
JAZZMIN_SETTINGS = {
    "site_title": "Ship Scanner Admin",
    "site_header": "Ship Scanner",
    "site_brand": "Ship Scanner",
    "welcome_sign": "Welcome to Ship Scanner Admin Panel",

    # Custom links (sidebar)
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

    # Scanner app icons
    "icons": {
        "scanner.ScanLog": "fas fa-history",
    },

    "show_ui_builder": False,
}


JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",           # Light theme
    "dark_mode_theme": None,     # Disable dark mode
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


# ====================================================
#              NGROK COMPATIBLE SETTINGS
# ====================================================

# Ngrok üçün CSRF icazəsi
CSRF_TRUSTED_ORIGINS = [
    "http://38.242.145.252:8010",
    "https://*.ngrok-free.app",
    "https://*.ngrok.app",
    "https://*.ngrok.io",
]

# Ngrok HTTPS forward fix
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Ngrok + Admin + Login üçün cookie düzəlişləri
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
