from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from commits.serializers import RegisterSerializer
from commits.logger import Log as log

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        log.success(message=f"User '{request.data['username']}' created successfully.")
        return Response({"message": "User registered successfully!"})
    return Response(serializer.errors, status=400)
