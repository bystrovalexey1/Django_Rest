from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from dotenv import load_dotenv
from rest_framework.filters import OrderingFilter

from .models import CustomUser, Payments
from .serializers import PaymentsSerializer, UserSerializer

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
