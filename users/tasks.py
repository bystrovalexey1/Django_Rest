from django.utils import timezone

from config.settings import DEFAULT_FROM_EMAIL
from users.models import CustomUser
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_sub_information(message, email):
    send_mail(
        subject="Информирование о статусе подписки",
        message=f"Здравствуйте!\n" f"{message}",
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )


@shared_task
def block_the_user():
    today = timezone.now().today().date()
    users = CustomUser.objects.all()
    for user in users:
        if (
            user.is_active
            and user.last_login
            and ((today - user.last_login.date()).days > 30)
        ):
            user.is_active = False
            user.save()
            print(f"Деактивирован пользователь {user.id}")
