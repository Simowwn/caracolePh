from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserInvitation
from django.core.mail import send_mail
from django.conf import settings
 
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

    email = serializers.EmailField(write_only=True)
    is_invited = serializers.BooleanField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    token = serializers.CharField(read_only=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].choices = self.get_email_choices()
    
    class Meta:
        model = UserInvitation
        fields = ['id', 'email', 'is_invited', 'expires_at', 'created_at', 'token']
         
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
        # Automatically set is_invited to True when creating
        validated_data['is_invited'] = True
        email = validated_data.pop('email')
        user = User.objects.get(email=email)
        invitation = UserInvitation.objects.create(user=user, **validated_data)
        
        # Send invitation email
        self.send_invitation_email(invitation)
        return invitation

    def send_invitation_email(self, invitation):
        # Generate the invitation URL with token instead of UUID
        invitation_url = f"{settings.FRONTEND_URL}/accept-invitation?token={invitation.token}"
        
        # Create plain text email message
        message = f"""
Hello,

You have been invited to join the Caracole PH Admin platform.

To accept your invitation, please click or copy-paste this link in your browser:
{invitation_url}

This invitation will expire on {invitation.expires_at.strftime('%Y-%m-%d %H:%M:%S')}.
If you did not request this invitation, please ignore this email.

Best regards,
The Caracole PH Team
"""
        
        # Send email
        send_mail(
            subject='Invitation to Caracole PH Admin',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.user.email],
            fail_silently=False,
        )


class InvitedRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email','password','first_name','last_name','token']
        extra_kwargs = {
            'email' : {'read_only':True}
        }
    
    def validate(self, value):
        # Create a copy of the value to avoid modifying the original QueryDict
        data = value.copy()  
        user = User.objects.filter(auth_token=data['token']).first()
        if not user:
            raise serializers.ValidationError("Invalid token")
        
        invitation = Invitation.objects.filter(
            user=user,
            is_invited=True,
            is_registered=False,
        ).first()

        if not invitation:
            raise serializers.ValidationError("Invalid or Expired Invitation")

        return data  # Return the modified copy instead of the original
    
    def create(self, validated_data):
        token = validated_data.pop('token')
        user = User.objects.get(auth_token=token)
        invitation = user.invitations.get(is_invited=True)

        user.set_password(validated_data['password'])
        user.first_name = validated_data.get('first_name', '')
        user.last_name = validated_data.get('last_name', '')
        user.save()

        invitation.is_registered = True
        invitation.save()

        return user