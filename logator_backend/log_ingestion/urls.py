from django.urls import path
from .views import log_ingestion_view, LogRetrievalAPIView

urlpatterns = [
    path('ingest/', log_ingestion_view, name='log-ingest'),
    path('retrieve/<int:service_id>/', LogRetrievalAPIView.as_view(), name='log-retrieve'),
]