from django import views
from rest_framework.views import APIView
from rest_framework.response import HttpResponse
from rest_framework import generics, serializers
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from .authentication import ScannerTokenAuthentication
from .auth_utils import generate_token
from .serializers import (StartupFormSerializer, 
                          StartupTeamMemberSerializer, 
                          LoginSerializer)

from .models import (StartupForm, 
                     StartupTeamMember, 
                     AuthUsers)


@extend_schema(
    request=LoginSerializer,
    responses={200: serializers.DictField()}
)
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = ScannerUser.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response({"detail": "Invalid username or password"}, status=401)

        token = generate_token(user.id)
        return Response({"token": token}, status=200)