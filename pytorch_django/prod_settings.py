""" Production Settings """
import django_heroku

# default: use settings from main settings.py if not overwritten
from .settings import *

from django.core.management.utils import get_random_secret_key
############
# SECURITY #
############

DEBUG = False

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', default=get_random_secret_key())

ALLOWED_HOSTS = ['img-captioning.herokuapp.com']

# Activate Django-Heroku.
django_heroku.settings(locals())

