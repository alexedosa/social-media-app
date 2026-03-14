from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CreateAccountSerializer, LoginSerializer

class Register(APIView):
    permission_classes = [AllowAny]
    #Form View
    def post(self, request):
        serialized_data = CreateAccountSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            return Response(
                {"msg":"User Created successfully"}, status=201
            )
        return Response (
            {"msg" : "Err occured somewhere, please try again."}, status=400
        )
    
class Login(APIView):
    def post(self, request):
        self.permission_classes = [AllowAny]
        serialized_data = LoginSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            user = serialized_data.validated_data['user']
            refresh_token = RefreshToken.for_user(user)

            return Response(
                {
                    "access": str(refresh_token.access_token),
                    "refresh": str(RefreshToken),
                    "user": {
                        "id" : user.id,
                        "email" : user.email
                    } 
                }
            )
