from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, UpdateAPIView, get_object_or_404
from dotenv import load_dotenv
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson
from .models import CustomUser, Payments, Follow
from .serializers import PaymentsSerializer, UserSerializer, FollowSerializer
from users.tasks import send_sub_information
from .services import create_stripe_product, create_stripe_session, create_stripe_price

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
        course_id = self.request.data.get("courses")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Follow.objects.filter(user=user, courses=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = f"подписка на курс {course_item} удалена"
            send_sub_information.delay(message, user.email)
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            sub = Follow.objects.create(user=user, courses=course_item)
            message = f"подписка на курс {course_item} добавлена"
            sub.save()
            send_sub_information.delay(message, user.email)
        # Возвращаем ответ в API
        return Response({"message": message})


class PaymentsCreateAPIView(CreateAPIView):
    serializer_class = PaymentsSerializer

    def post(self, request, content_type, content_id):
        try:
            if content_type == "lesson":
                content = get_object_or_404(Lesson, id=content_id)
                pay_lesson = content
                pay_course = None
            elif content_type == "course":
                content = get_object_or_404(Course, id=content_id)
                pay_lesson = None
                pay_course = content
            else:
                return Response(
                    {"error": "Неверный тип контента"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Проверяем, создан ли уже продукт в Stripe
            if not content.stripe_product_id:
                stripe_product_id = create_stripe_product(content)
                if not stripe_product_id:
                    return Response(
                        {"error": "Ошибка создания продукта в Stripe"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            stripe_price = create_stripe_price(content)
            if not stripe_price:
                return Response(
                    {"error": "Ошибка создания цены в Stripe"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            session_id, payment_link = create_stripe_session(stripe_price.id)
            if not session_id or not payment_link:
                return Response(
                    {"error": "Ошибка создания сессии оплаты"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            payment = Payments.objects.create(
                user=request.user,
                pay_lesson=pay_lesson,
                pay_course=pay_course,
                payment_amount=content.price,
                session_id=session_id,
                link=payment_link,
                payment_method="card",
            )

            serializer = self.serializer_class(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
