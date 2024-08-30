from django.db import models
from service_registration.models import Service

class Log(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    log_level = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.service.name} - {self.log_level}"
