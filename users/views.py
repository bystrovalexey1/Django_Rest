from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from dotenv import load_dotenv
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course
from .models import CustomUser, Payments, Follow
from .serializers import PaymentsSerializer, UserSerializer, FollowSerializer
from users.tasks import send_sub_information

load_dotenv(override=True)


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["pay_course", "pay_lesson"]
    ordering_fields = ["pay_date"]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class FollowUpdateAPIView(UpdateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('courses')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Follow.objects.filter(user=user, courses=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = f'подписка на курс {course_item} удалена'
            send_sub_information.delay(message, user.email)
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            sub = Follow.objects.create(user=user, courses=course_item)
            message = f'подписка на курс {course_item} добавлена'
            sub.save()
            send_sub_information.delay(message, user.email)
        # Возвращаем ответ в API
        return Response({"message": message})
