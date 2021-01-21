import os

from .common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Only git hub environs have this env var, for github actions
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

# Use development server database url
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config("LOCAL_DB_NAME"),
            'USER': config("LOCAL_DB_USER"),
            'PASSWORD': config("LOCAL_DB_PASSWORD"),
            'HOST': config("LOCAL_DB_HOST"),
            'PORT': config("LOCAL_DB_PORT")
        }
    }

