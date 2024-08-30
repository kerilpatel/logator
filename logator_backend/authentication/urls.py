# auth/urls.py
from django.urls import path
from .views import UserRegistrationAPIView, login_view

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', login_view, name='user-login'),
]
