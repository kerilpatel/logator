from django.db import models
from service_registration.models import Service

class Log(models.Model):
    class LogLevelChoices(models.TextChoices):
        DEBUG = 'DEBUG', 'Debug'
        INFO = 'INFO', 'Info'
        WARNING = 'WARNING', 'Warning'
        ERROR = 'ERROR', 'Error'
        CRITICAL = 'CRITICAL', 'Critical'

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    log_level = models.CharField(max_length=10, choices=LogLevelChoices.choices)
    log_tag = models.CharField(max_length=50, blank=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.service.name} - {self.log_level}"