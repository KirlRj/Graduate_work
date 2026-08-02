from rest_framework import status
from rest_framework.test import APITestCase

from .models import OTPCode, User


class SendCodeViewTest(APITestCase):
    def test_send_code_success(self):
        response = self.client.post("/users/send-code/", {"phone": "89991234567"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(OTPCode.objects.filter(phone="89991234567").exists())

    def test_send_code_invalid_phone(self):
        response = self.client.post("/users/send-code/", {"phone": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VerifyCodeViewTest(APITestCase):
    def setUp(self):
        self.phone = "89991234567"
        self.code = "1234"
        OTPCode.objects.create(phone=self.phone, code=self.code)

    def test_verify_code_success(self):
        response = self.client.post(
            "/users/verify-code/", {"phone": self.phone, "code": self.code}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertTrue(User.objects.filter(phone=self.phone).exists())

    def test_verify_code_invalid(self):
        response = self.client.post(
            "/users/verify-code/", {"phone": self.phone, "code": "0000"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(phone="89991234567", referral_code="ABC123")
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        response = self.client.get("/users/profile-view/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "89991234567")

    def test_activate_invite_code(self):
        other_user = User.objects.create(phone="89997654321", referral_code="XYZ999")
        response = self.client.post("/users/profile-view/", {"referral_code": "XYZ999"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_own_invite_code(self):
        response = self.client.post("/users/profile-view/", {"referral_code": "ABC123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_nonexistent_invite_code(self):
        response = self.client.post("/users/profile-view/", {"referral_code": "XXXXXX"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
