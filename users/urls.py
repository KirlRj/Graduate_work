from django.urls import path

from users.views import SendCodeView, VerifyCodeView, ProfileView, SendCodeTemplateView, VerifyCodeTemplateView, ProfileTemplateView

urlpatterns = [
    path("profile-view/", ProfileView.as_view(), name="profile_view"),
    path("send-code/", SendCodeView.as_view(), name="send_code"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify_code"),

    # Templates
    path("", SendCodeTemplateView.as_view(), name="send_code_template"),
    path("verify/", VerifyCodeTemplateView.as_view(), name="verify_code_template"),
    path("profile/", ProfileTemplateView.as_view(), name="profile_template"),
]