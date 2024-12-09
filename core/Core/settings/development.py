
from .common import *


# Email
domain = os.getenv("Domain")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp4dev"
EMAIL_PORT = "25"
EMAIL_USE_TLS = False

EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""



