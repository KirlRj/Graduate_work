from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=11, unique=True)
    referral_code = models.CharField(max_length=6, unique=True)
    users_referral_code = models.CharField(max_length=6, unique=False, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class OTPCode(models.Model):
    phone = models.CharField(max_length=11, unique=False)
    code = models.CharField(max_length=4, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждений'
