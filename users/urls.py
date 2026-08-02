from django.urls import path

from users.views import SendCodeView, VerifyCodeView, ProfileView


urlpatterns = [
    path("profile-view/", ProfileView.as_view(), name="profile_view"),
    path("send-code/", SendCodeView.as_view(), name="send_code"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify_code"),
]