
from .common import *
import os
from dotenv import load_dotenv


# Email
Domain= os.getenv('Domain', '').split(',')[0].strip()
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp4dev"
EMAIL_PORT = "25"
EMAIL_USE_TLS = False

EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = "admin@admin.com"

# Email



