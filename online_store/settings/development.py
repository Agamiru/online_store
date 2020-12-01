from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("LOCAL_DB_NAME"),
        'USER': config("LOCAL_DB_USER"),
        'PASSWORD': config("LOCAL_DB_PASSWORD"),
        'HOST': config("LOCAL_DB_HOST"),
        'PORT': config("LOCAL_DB_PORT", default="")

    }
}