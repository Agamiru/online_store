from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("NAME"),
        'USER': config("USER"),
        'PASSWORD': config("PASSWORD"),
        'HOST': config("HOST"),
        'PORT': config("PORT", default="")

    }
}