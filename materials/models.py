from django.db import models

from users.models import CustomUser


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название курса')
    preview = models.ImageField(upload_to="course/", blank=True, null=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание курса")
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Укажите автора",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["id"]


class Lesson(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название урока')
    preview = models.ImageField(upload_to="course/", blank=True, null=True)
    description = models.TextField(null=True, blank=True, verbose_name="Описание урока")
    video_url = models.CharField(max_length=300, verbose_name='Ссылка на видео')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите курс",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        help_text="Укажите автора",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["id"]