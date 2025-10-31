from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Course, Lesson
from users.models import CustomUser, Follow


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = CustomUser.objects.create(email="bystrovalexey@sky.pro")
        self.course = Course.objects.create(
            name="Языки программирования",
            description="Обучение языкам программирования",
            owner=self.user,
        )
        self.lesson = Lesson.objects.create(
            name="Python",
            description="Python course",
            video_url="https://www.youtube.com/351a",
            owner=self.user,
            course=self.course,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        url = reverse("materials:lesson_create")
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "test",
            "video_url": "https://www.youtube.com/test",
            "description": "test",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_bad_youtube(self):
        """Тестирование ошибки при неправильной ссылке на видео"""
        url = reverse("materials:lesson_create")
        self.client.force_authenticate(user=self.user)
        data = {
            "name": "JAVA Script",
            "description": "Java Script course",
            "course": self.course.pk,
            "owner": self.user.pk,
            "video_url": "https://www.youtube.ru/test",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_retrieve(self):
        """Тестирование вывода урока"""
        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["name"], self.lesson.name)

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "DRF"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "DRF"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video_url": self.lesson.video_url,
                    "name": self.lesson.name,
                    "preview": None,
                    "description": self.lesson.description,
                    "course": self.course.pk,
                    "owner": self.user.pk
                },
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

class FollowTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="bystrovalexey@sky.pro")
        self.course = Course.objects.create(name="Подписка", description="Тест подписки", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("users:follow-check")
        data = {"courses": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": f'подписка на курс {self.course.title} добавлена'})

    def test_unsubscribe(self):
        url = reverse("users:follow-check")
        data = {"courses": self.course.pk}
        Follow.objects.create(courses=self.course, user=self.user)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': f'подписка на курс {self.course.title} удалена'})