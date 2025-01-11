from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# queue parameter you can select the worker 
@shared_task(name='accounts.validation_email', queue='queue_one')
def send_validation_email(email, validation_link):
    subject = 'Validate Your Account'
    html_message = render_to_string('email/validation_email.html', {'validation_link': validation_link})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = email

    try:
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        logger.info('Email sent successfully')
    except Exception as e:
        logger.error(f'Error sending email: {e}')



@shared_task(name='accounts.reset_password', queue='queue_one')
def send_reset_password_email(email, reset_link):
    subject = 'Reset Password'
    html_message = render_to_string('email/reset_password.html', {'Reset_link': reset_link})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = email

    try:
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        logger.info('Email sent successfully')
    except Exception as e:
        logger.error(f'Error sending email: {e}')