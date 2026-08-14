from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import User

phone_validator = RegexValidator(
    regex=r"^8\d{10}$",
    message="Номер телефона должен начинаться с 8 и содержать 11 цифр",
)


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, validators=[phone_validator])


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=4)


class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class ProfileSerializer(serializers.Serializer):
    phone = serializers.CharField()
    referral_code = serializers.CharField()
    users_referral_code = serializers.CharField(allow_null=True)
    referrals = serializers.ListField(child=serializers.CharField())


class ActivateInviteSerializer(serializers.Serializer):
    referral_code = serializers.CharField(max_length=6)
