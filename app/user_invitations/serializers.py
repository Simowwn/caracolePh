from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserInvitation
 
User = get_user_model()
 
class UserInvitationSerializer(serializers.ModelSerializer):
    def get_email_choices(self):
        # Get all inactive users that are not staff or superuser
        users = User.objects.filter(
            is_active=False,
            is_staff=False,
            is_superuser=False
        )
        return [(user.email, user.email) for user in users]

    email = serializers.ChoiceField(choices=[], write_only=True)
    is_invited = serializers.BooleanField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].choices = self.get_email_choices()
    
    class Meta:
        model = UserInvitation
        fields = ['id','email','is_invited','expires_at','created_at']
         
    def validate_email(self, value):
        try: 
            user = User.objects.get(email=value)
            if user.is_active:
                raise serializers.ValidationError("Cannot Invite active users. ")
            if user.is_staff:
                raise serializers.ValidationError("Cannot Invite is alreadu staff")
            if user.is_superuser:
                raise serializers.ValidationError("Cannot Invite is already admin")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
    
    def create(self, validated_data):
        email = validated_data.pop('email')
        user = User.objects.get(email=email)
        invitation = UserInvitation.objects.create(user=user, **validated_data)
        
        # Here you could add email sending logic
        return invitation