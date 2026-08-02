from django.contrib import admin

from .models import OTPCode, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone", "referral_code", "users_referral_code")


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "timestamp")
