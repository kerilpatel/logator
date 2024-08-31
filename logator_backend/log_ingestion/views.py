import json
import hmac
import hashlib
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LogSerializer
from .models import Log
from service_registration.models import Service

class LogRetrievalAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id, user=request.user)
            logs = Log.objects.filter(service=service)
            serializer = LogSerializer(logs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Service.DoesNotExist:
            return Response({"error": "Service not found or you do not have access to it"}, status=status.HTTP_400_BAD_REQUEST)

# API Security Requirements:
# - JSON Format: Compact, no spaces, UTF-8 encoded.
# - HMAC Signature: SHA-256, generated from the concatenated string of the JSON payload and a UNIX timestamp.
# - Timestamp: Sent as a UNIX timestamp in seconds, must be within 5 minutes of the server time.

def verify_hmac_signature(secret_key, message, client_signature, client_timestamp):
    try:
        parsed_message = json.loads(message)
        standardized_message = json.dumps(parsed_message, separators=(',', ':'))
    except json.JSONDecodeError:
        standardized_message = message
    
    message_bytes = (standardized_message + client_timestamp).encode('utf-8')
    secret_bytes = secret_key.encode('utf-8')
    server_signature = hmac.new(secret_bytes, message_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(server_signature, client_signature)

def api_key_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        api_key = request.headers.get('Api-Key')
        client_signature = request.headers.get('Hmac-Signature')
        client_timestamp = request.headers.get('Timestamp')

        if not api_key or not client_signature or not client_timestamp:
            return JsonResponse({'error': 'Missing authentication headers'}, status=403)

        try:
            service = Service.objects.get(api_key=api_key)
            request.service = service

            if not verify_hmac_signature(service.secret_key, request.body.decode('utf-8'), client_signature, client_timestamp):
                return JsonResponse({'error': 'Invalid HMAC signature'}, status=403)

            if abs(int(time.time()) - int(client_timestamp)) > 300:  # 5 minutes tolerance
                return JsonResponse({'error': 'Timestamp is too old'}, status=403)

        except Service.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key'}, status=403)

        return view_func(request, *args, **kwargs)
    return _wrapped_view

@csrf_exempt
@api_key_required
def log_ingestion_view(request):
    service = request.service
    log_data = json.loads(request.body.decode('utf-8'))
    Log.objects.create(
        service=service,
        timestamp=log_data['timestamp'],
        log_level=log_data['log_level'],
        message=log_data['message']
    )
    return JsonResponse({"status": "Log ingested"}, status=201)