from django.urls import path, include
from .views import LoginAPIView, LogoutAPIView, RegisterAPIView


urlpatterns = [
    path("api/v1/logout", LoginAPIView.as_view()), 
    path("api/v1/logout", LogoutAPIView.as_view()),
    path("api/v1/register", RegisterAPIView.as_view()),

]
