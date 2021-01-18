import os

from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("LOCAL_DB_NAME", default=""),
        'USER': config("LOCAL_DB_USER", default=""),
        'PASSWORD': config("LOCAL_DB_PASSWORD", default=""),
        'HOST': config("LOCAL_DB_HOST", default=""),
        'PORT': config("LOCAL_DB_PORT", default="")
    }
}

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github_actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }