from django.urls import path

from .views import (JudgeRegisterAPIView, LawyerRegisterAPIView,
                    ListLawyersAPIView, ListPreTrialsAPIView, LoginAPIView,
                    LogoutAPIView, UserRegisterAPIView)

urlpatterns = [
    path("api/v1/login/", LoginAPIView.as_view()),
    path("api/v1/logout/", LogoutAPIView.as_view()),
    path("api/v1/register/client/", UserRegisterAPIView.as_view()),
    path("api/v1/register/lawyer/", LawyerRegisterAPIView.as_view()),
    path("api/v1/register/judge/", JudgeRegisterAPIView.as_view()),
    path("api/v1/list/lawyer/", ListLawyersAPIView.as_view()),
    path("api/v1/list/pretrial/", ListPreTrialsAPIView.as_view()),
]
