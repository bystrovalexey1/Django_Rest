from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Payments, CustomUser, Follow


class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields = [
            "user",
            "pay_date",
            "pay_course",
            "pay_lesson",
            "payment_amount",
            "payment_method",
            "session_id",
            "link",
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
