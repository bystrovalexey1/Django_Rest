from django.db import models
from django.contrib.auth.models import AbstractUser

from materials.models import Course, Lesson


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    token = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email


class Payments(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
        null=True,
        blank=True,
    )
    pay_date = models.DateTimeField(auto_now_add=True, verbose_name="дата оплаты")
    pay_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплата курса",
        help_text="Укажите курс",
        null=True,
        blank=True,
    )
    pay_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплата урока",
        help_text="Укажите урок",
        null=True,
        blank=True,
    )
    payment_amount = models.IntegerField(verbose_name='сумма оплаты')
    PAYMENT_METHOD_CHOICES = [
        ("наличные", "Наличные"),
        ("перевод на счет", "Перевод на счет"),
    ]
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, default="наличные")

    def __str__(self):
        return f'{self.user} - {self.pay_date}'

