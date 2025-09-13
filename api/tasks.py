from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_delete_notification_email(email, username):
    subject = "Delete Accout Notification"
    message = f"Dear, {username} your account has been succesfully deleted"
    send_mail(subject=subject, message=message,from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email])
