import random
import string
import time

from django.shortcuts import redirect, render
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPCode, User
from .serializers import SendCodeSerializer, VerifyCodeSerializer


# Create your views here.
class SendCodeView(APIView):
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            code = str(random.randint(1000, 9999))
            time.sleep(1)
            OTPCode.objects.create(phone=phone, code=code)
            return Response(
                {"message": f"Код {code} подтверждения отправлен на номер {phone}"}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            code = serializer.validated_data["code"]

            otp = OTPCode.objects.filter(phone=phone, code=code).first()
            if not otp:
                return Response(
                    {"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST
                )

            otp.delete()

            user, created = User.objects.get_or_create(phone=phone)
            if created:
                chars = string.ascii_uppercase + string.digits
                user.referral_code = "".join(random.choices(chars, k=6))
                user.save()

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        referrals = User.objects.filter(users_referral_code=user.referral_code)
        return Response(
            {
                "phone": user.phone,
                "referral_code": user.referral_code,
                "users_referral_code": user.users_referral_code,
                "referrals": [u.phone for u in referrals],
            }
        )

    def post(self, request):
        user = request.user
        referral_code = request.data.get("referral_code")

        if user.users_referral_code:
            return Response(
                {"error": "Вы уже активировали инвайт-код"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not User.objects.filter(referral_code=referral_code).exists():
            return Response(
                {"error": "Инвайт-код не найден"}, status=status.HTTP_400_BAD_REQUEST
            )

        if referral_code == user.referral_code:
            return Response(
                {"error": "Нельзя активировать свой собственный инвайт-код"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.users_referral_code = referral_code
        user.save()
        return Response({"message": "Инвайт-код активирован"})


class SendCodeTemplateView(View):
    def get(self, request):
        return render(request, "users/send_code.html")

    def post(self, request):
        phone = request.POST.get("phone")
        code = str(random.randint(1000, 9999))
        time.sleep(1)
        OTPCode.objects.create(phone=phone, code=code)
        request.session["phone"] = phone
        request.session["code"] = code
        return redirect("verify_code_template")


class VerifyCodeTemplateView(View):
    def get(self, request):
        code = request.session.get("code")
        phone = request.session.get("phone")
        return render(request, "users/verify_code.html", {"phone": phone, "code": code})

    def post(self, request):
        phone = request.POST.get("phone")
        code = request.POST.get("code")
        otp = OTPCode.objects.filter(phone=phone, code=code).first()
        if not otp:
            return render(
                request,
                "users/verify_code.html",
                {"phone": phone, "error": "Неверный код"},
            )
        otp.delete()
        user, created = User.objects.get_or_create(phone=phone)
        if created:
            chars = string.ascii_uppercase + string.digits
            user.referral_code = "".join(random.choices(chars, k=6))
            user.save()
        request.session["user_id"] = str(user.id)
        return redirect("profile_template")


class ProfileTemplateView(View):
    def get(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("send_code_template")
        user = User.objects.get(id=user_id)
        referrals = User.objects.filter(users_referral_code=user.referral_code)
        return render(
            request,
            "users/profile.html",
            {"user": user, "referrals": [u.phone for u in referrals]},
        )

    def post(self, request):
        user_id = request.session.get("user_id")
        user = User.objects.get(id=user_id)
        referral_code = request.POST.get("referral_code")

        if user.users_referral_code:
            error = "Вы уже активировали инвайт-код"
        elif referral_code == user.referral_code:
            error = "Нельзя активировать свой собственный инвайт-код"
        elif not User.objects.filter(referral_code=referral_code).exists():
            error = "Инвайт-код не найден"
        else:
            user.users_referral_code = referral_code
            user.save()
            error = None

        referrals = User.objects.filter(users_referral_code=user.referral_code)
        return render(
            request,
            "users/profile.html",
            {"user": user, "referrals": [u.phone for u in referrals], "error": error},
        )
