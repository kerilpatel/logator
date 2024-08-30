from django.db import models
from django.contrib.auth.models import User
import secrets
import uuid


class Service(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    secret_key = models.CharField(max_length=64, default=secrets.token_hex(32), editable=False)

    def __str__(self):
        return self.name
