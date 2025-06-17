from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from materials.models import Course, Lesson
from users.models import Payments, CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):

        payments = {"user": CustomUser(id=2), "pay_course": Course(id=1), "pay_lesson": Lesson(id=2), "payment_amount": 100, "payment_method": "наличные"}

        payment, created = Payments.objects.get_or_create(**payments)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Успешно создан"))