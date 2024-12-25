from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# queue parameter you can select the worker 
@shared_task(name='accounts.validation_email', queue='queue_one')
def send_validation_email(email, validation_link):
    subject = 'Validate Your Account'
    html_message = render_to_string('validation_email.html', {'validation_link': validation_link})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to = email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)