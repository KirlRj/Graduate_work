from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

phone_validator = RegexValidator(
    regex=r"^8\d{10}$",
    message="Номер телефона должен начинаться с 8 и содержать 11 цифр",
)


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Номер телефона обязателен")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True, validators=[phone_validator])
    referral_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    users_referral_code = models.CharField(
        max_length=6, unique=False, null=True, blank=True
    )
    username = None

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class OTPCode(models.Model):
    phone = models.CharField(max_length=11, unique=False)
    code = models.CharField(max_length=4, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = "Код подтверждения"
        verbose_name_plural = "Коды подтверждений"
