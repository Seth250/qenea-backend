from __future__ import annotations

import smtplib
from typing import Sequence

from django.core.mail import EmailMultiAlternatives

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(name='send email to user')
def send_email(subject: str, body: str, to: str | Sequence[str], from_email: str | None = None,
               html_content: str | None = None, fail_silently: bool = False):
    if isinstance(to, str):
        to = [to]

    email = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=to)
    if html_content is not None:
        email.attach_alternative(html_content, 'text/html')

    try:
        return email.send(fail_silently=fail_silently)
    except smtplib.SMTPException as e:
        logger.error(e)
