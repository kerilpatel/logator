from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer

class ServiceRegistrationAPIView(APIView):
    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            response_data = {
                "api_key": service.api_key,
                "secret_key": service.secret_key
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, service_id=None):
        if service_id:
            try:
                service = Service.objects.get(id=service_id)
                serializer = ServiceSerializer(service)
                return Response(serializer.data)
            except Service.DoesNotExist:
                return Response({"error": "Service not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data)