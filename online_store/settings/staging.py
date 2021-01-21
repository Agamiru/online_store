import os

from dj_database_url import parse as dburl

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

# Use staging server database url
else:
    DATABASES = {
        'default': config("DATABASE_URL", cast=dburl)
    }
