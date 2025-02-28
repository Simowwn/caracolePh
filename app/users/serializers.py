from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

class EmailAndPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                raise serializers.ValidationError("User is inactive")
            if not user.is_staff:
                raise serializers.ValidationError("User is not an administrator")
            
            if not check_password(password, user.password):
                raise serializers.ValidationError("Invalid password")
                
            return {"user": user}
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")