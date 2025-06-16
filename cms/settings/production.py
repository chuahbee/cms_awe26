from .base import *
from decouple import config, Csv

DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
# DEBUG = False

ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())

SECRET_KEY = config("DJANGO_SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config("DJANGO_DB_NAME"),
        'USER': config("DJANGO_DB_USER"),
        'PASSWORD': config("DJANGO_DB_PASSWORD"),
        'HOST': config("DJANGO_DB_HOST", default="localhost"),
        'PORT': config("DJANGO_DB_PORT", default="3306"),
    }
}

# STATIC_ROOT = config("DJANGO_STATIC_ROOT", default="/home/smaruina/awe25/static/img")


# try:
#     from .local import *
# except ImportError:
#     pass
