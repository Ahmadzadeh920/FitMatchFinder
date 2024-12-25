# To make sure that your Celery app is loaded when you start Django, you should add it to
from .celery import app as celery_app

__all__ = ['celery_app']

# When starting Celery with this command, you provide the name of the module that contains your Celery app instance, "app", to -A.