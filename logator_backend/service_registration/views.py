from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Service
from .serializers import ServiceSerializer

class ServiceRegistrationAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save(user=request.user)
            response_data = {
                "api_key": service.api_key,
                "secret_key": service.secret_key
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            error_messages = {field: ", ".join(map(str, msgs)) for field, msgs in errors.items()}
            consolidated_errors = "; ".join([f"{field}: {msgs}" for field, msgs in error_messages.items()])
            return Response({"error": consolidated_errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, service_id=None):
        if service_id:
            try:
                service = Service.objects.get(id=service_id)
                serializer = ServiceSerializer(service)
                return Response(serializer.data)
            except Service.DoesNotExist:
                return Response({"error": "Service not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data)