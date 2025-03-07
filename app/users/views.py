from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login
from .serializers import EmailAndPasswordSerializer, UserUpdateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics
from django.shortcuts import get_object_or_404

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
                    "first_name": existing_user.first_name,
                    "last_name": existing_user.last_name,
                    "is_superuser": existing_user.is_superuser,
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
        users = []
        for user in self.queryset.all():
            users.append({
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'groups': [group.name for group in user.groups.all()],
                'user_permissions': [perm.codename for perm in user.user_permissions.all()]
            })
        return Response(users, status=status.HTTP_200_OK)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserUpdateSerializer

    def get(self, request, user_id):
        try:
            if not request.user.is_superuser:
                return Response({
                    'error': 'Only superusers can view user information'
                }, status=status.HTTP_403_FORBIDDEN)
                
            user = get_object_or_404(User, id=user_id)
            serializer = self.serializer_class(user)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        try:
            if not request.user.is_superuser:
                return Response({
                    'error': 'Only superusers can edit user information'
                }, status=status.HTTP_403_FORBIDDEN)
                
            user = get_object_or_404(User, id=user_id)
            serializer = self.serializer_class(user, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_user = serializer.save()
                return Response({
                    'message': 'User updated successfully',
                    'user': {
                        'id': updated_user.id,
                        'email': updated_user.email,
                        'first_name': updated_user.first_name,
                        'last_name': updated_user.last_name,
                        'is_active': updated_user.is_active,
                        'is_staff': updated_user.is_staff,
                        'is_superuser': updated_user.is_superuser,
                        'date_joined': updated_user.date_joined,
                        'last_login': updated_user.last_login,
                        'groups': [group.name for group in updated_user.groups.all()],
                        'user_permissions': [perm.codename for perm in updated_user.user_permissions.all()]
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def _add_cors_headers(self, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, PUT, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        response["Access-Control-Allow-Credentials"] = "true"

    def options(self, request, *args, **kwargs):
        response = Response()
        self._add_cors_headers(response)
        return response