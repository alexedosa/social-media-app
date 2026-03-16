from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CreateAccountSerializer, LoginSerializer


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "User created successfully"}, status=201)
    
class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serialized_data = LoginSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            user = serialized_data.validated_data['user']
            refresh_token = RefreshToken.for_user(user)

            return Response(
                {
                    "access": str(refresh_token.access_token),
                    "refresh": str(refresh_token),
                    "user": {
                        "id" : user.id,
                        "email" : user.email,
                        "username": user.username
                    } 
                }
            )
