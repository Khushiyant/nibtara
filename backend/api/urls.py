from django.urls import path
from .views import LoginAPIView, LogoutAPIView, UserRegisterAPIView


urlpatterns = [
    path("api/v1/login", LoginAPIView.as_view()), 
    path("api/v1/logout", LogoutAPIView.as_view()),
    path("api/v1/register/client", UserRegisterAPIView.as_view()),
]
