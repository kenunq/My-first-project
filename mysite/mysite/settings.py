"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import logging.config
import os
import sys
from pathlib import Path

from celery.schedules import crontab
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "debug_toolbar",
    "tinymce",
    "channels",
    "channels_redis",
    "django_recaptcha",
    "CharPage",
    "user",
    "addons",
    "HomePage",
    "talants",
    "services",
    "support",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "common.middleware.count_users_online",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",  # debug toolbar
]

INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "mysite.asgi.application"
WSGI_APPLICATION = "mysite.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("POSTGRES_NAME"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST") if not bool(os.environ.get("RUN_FROM_DOCKER")) else "postgres",
        "PORT": config("POSTGRES_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"  # UTC+3

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "/static/"

if DEBUG and not bool(os.environ.get("RUN_FROM_DOCKER")):
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# user

AUTH_USER_MODEL = "user.User"
LOGIN_URL = "/user/login/"
LOGOUT_REDIRECT_URL = "/user/login/"
LOGIN_REDIRECT_URL = "/"

# captcha

RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY")

if "test" in sys.argv:
    CAPTCHA_TEST_MODE = True

# redis

REDIS_HOST = config("REDIS_HOST") if not os.environ.get("RUN_FROM_DOCKER") else "redis"
REDIS_PORT = config("REDIS_PORT")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# celery

CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/0"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    "clear-orders": {
        "task": "addons.tasks.clear_orders",
        "schedule": crontab(hour=4, minute=0),
    },
}

# Telegram

TELEBOT_ID = config("TELEBOT_ID")

# mail

EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 465
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMINS = [
    ("Admin", EMAIL_HOST_USER)
]  # Нужно для отправки писем через django.utils.log.AdminEmailHandler https://docs.djangoproject.com/en/3.2/ref/settings/#std-setting-ADMINS

SITE_ID = 1

PARENT_DOMAIN = ALLOWED_HOSTS[0]


# LOGGING
LOGGING_CONFIG = (
    None  # отключение настроек логинга по умолчанию https://docs.djangoproject.com/en/dev/topics/logging/#top
)

logging.config.dictConfig(
    {
        "version": 1,  # the dictConfig format version
        "disable_existing_loggers": False,  # retain the default loggers
        "formatters": {
            "verbose": {
                "format": "{levelname} --- {asctime} --- {module} --- {filename} --- {message}",
                "style": "{",
            },
            "simple": {
                "format": "{levelname} --- {message}",
                "style": "{",
            },
        },
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "file": {
                "level": "WARNING",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logging.log",
                "formatter": "verbose",
                "maxBytes": 1024 * 1024 * 5,  # 5MB максимальный размер файла
                "backupCount": 5,
            },
            "mail_admins": {
                "level": "ERROR",
                "class": "django.utils.log.AdminEmailHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "level": "INFO",
                "handlers": ["console", "mail_admins", "file"],
                "propagate": True,
            },
        },
    }
)

# tinymce

TINYMCE_DEFAULT_CONFIG = {
    "branding": False,
    "height": "650px",
    "width": "100%",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}

# payment
MERCHANT_ID = config("MERCHANT_ID")
SECRET_WORD = config("SECRET_WORD")
