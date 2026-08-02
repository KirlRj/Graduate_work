from rest_framework import serializers
from .models import User, OTPCode
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^8\d{10}$',
    message='Номер телефона должен начинаться с 8 и содержать 11 цифр'
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "phone", "referral_code", "users_referral_code"]


class OTPCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPCode
        fields = ['phone', 'code', 'timestamp']


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=4)

class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, validators=[phone_validator])