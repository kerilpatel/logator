from django.urls import path
from .views import ServiceRegistrationAPIView

urlpatterns = [
    path('services/', ServiceRegistrationAPIView.as_view(), name='service-registration'),
    path('services/<int:service_id>/', ServiceRegistrationAPIView.as_view(), name='service-detail'),
]
