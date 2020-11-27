from .common import *

from decouple import Csv
from dj_database_url import parse as dburl



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv)

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': config("DATABASE_URL", cast=dburl)
}