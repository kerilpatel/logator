from rest_framework import serializers
from .models import Log

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['service', 'timestamp', 'log_level', 'log_tag', 'message']
