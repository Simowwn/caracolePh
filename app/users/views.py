from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from .serializers import EmailAndPasswordSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = EmailAndPasswordSerializer

    def get(self, request, *args, **kwargs):
        response = Response({
            "message": "Please use POST to submit your credentials.",
            "required_fields": ["email", "password"]
        }, status=status.HTTP_200_OK)
        self._add_cors_headers(response)
        return response

    def post(self, request):
        try:
            data = request.data
            email = data.get("email")
            password = data.get("password")

            existing_user = User.objects.get(email=email, is_staff=True)  # Adjust as needed
            is_password_correct = check_password(password, existing_user.password)

            if not is_password_correct:
                return Response(
                    {"message": "Invalid password. Try again."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            login(request, existing_user)

            refresh = RefreshToken.for_user(existing_user)

            response = Response(
                {
                    "message": "Login successful.",
                    "user_id": existing_user.id,
                    "refresh_token": str(refresh),
                    "access_token": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
            
            self._add_cors_headers(response)
            return response
            
        except User.DoesNotExist:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            response = Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            self._add_cors_headers(response)
            return response
            
    def options(self, request, *args, **kwargs):
        response = Response()
        self._add_cors_headers(response)
        return response

    def _add_cors_headers(self, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        response["Access-Control-Allow-Credentials"] = "true"

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    
    def get(self, request, *args, **kwargs):
        users = self.queryset.values('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
        return Response(list(users), status=status.HTTP_200_OK)