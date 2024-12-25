import os
from celery import Celery
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Core.settings.common")

app = Celery("Core")
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# The celery.py file can also optionally contain scheduled tasks configuration.

app.conf.beat_schedule = {
    "run-every-10-seconds": {
        "task": "accounts.tasks.send_feedback_email_task",
        "schedule": timedelta(seconds=10),
    },
    
}
