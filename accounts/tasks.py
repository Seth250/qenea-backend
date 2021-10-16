import logging
import smtplib
from typing import Optional

from django.core.mail import EmailMultiAlternatives

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name='send email to user')
def send_email(subject: str, body: str, to: str, fail_silently: bool = False, html_content: Optional[str] = None):
    email = EmailMultiAlternatives(subject=subject, body=body, to=[to])
    if html_content:
        email.attach_alternative(html_content, 'text/html')

    try:
        return email.send(fail_silently=fail_silently)
    except smtplib.SMTPException as e:
        logger.error(e)
