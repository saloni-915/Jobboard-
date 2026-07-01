from celery import shared_task
from django.core.mail import send_mail


@shared_task(
    autoretry_for=(Exception,),
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=60,
)
def send_welcome_email(first_name, user_email):

    send_mail(
        "Welcome to Job Board!",
        f"Hi {first_name}, your account has been created successfully.",
        None,
        [user_email],
    )
