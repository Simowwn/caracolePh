from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserInvitation
from django.core.mail import send_mail
from django.conf import settings
 
User = get_user_model()
 
class UserInvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)  # ✅ Accepts input

    is_invited = serializers.BooleanField(read_only=True)
    expires_at = serializers.DateTimeField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = UserInvitation
        fields = ['id', 'email', 'is_invited', 'expires_at', 'created_at', 'token']

    def create(self, validated_data):
        email = validated_data.pop("email")  # ✅ Extract before creating UserInvitation

        # Get or create the user
        user, created = User.objects.get_or_create(email=email, defaults={"is_active": False})

        # Create UserInvitation with the user instance
        invitation = UserInvitation.objects.create(user=user, **validated_data)

        # Send invitation email
        self.send_invitation_email(invitation)

        return invitation

    def to_representation(self, instance):
        """ Ensure email is included in the response from the User model """
        data = super().to_representation(instance)
        data["email"] = instance.user.email  # ✅ Fetch email from the related User
        return data

    def send_invitation_email(self, invitation):
        invitation_url = f"{settings.FRONTEND_URL}/accept-invitation?token={invitation.token}"
        message = f"""
Hello,

You have been invited to join the Caracole PH Admin platform.

To accept your invitation, please click or copy-paste this link in your browser:
{invitation_url}

This invitation will expire on {invitation.expires_at.strftime('%Y-%m-%d %H:%M:%S')}.

Best regards,
The Caracole PH Team
"""

        send_mail(
            subject='Invitation to Caracole PH Admin',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invitation.user.email],
            fail_silently=False,
        )


class InvitedRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)  # ✅ Keep read_only but also include it in `to_representation`

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def to_representation(self, instance):
        """ Ensure email is included in the form """
        data = super().to_representation(instance)
        data["email"] = instance.email  # ✅ Manually add email to response
        return data
    
    def validate(self, value):
        token = self.context.get("token")  # Get token from context instead of request data

        if not token:
            raise serializers.ValidationError("Missing invitation token.")

        invitation = UserInvitation.objects.filter(token=token, is_invited=False).first()

        if not invitation:
            raise serializers.ValidationError("Invalid or expired invitation.")

        if invitation.is_expired():
            raise serializers.ValidationError("This invitation has expired.")

        value["user"] = invitation.user  # Attach the user to validated data
        return value




    
    def create(self, validated_data):
        token = validated_data.pop("token")
        invitation = UserInvitation.objects.filter(token=token, is_invited=True).first()

        if not invitation:
            raise serializers.ValidationError("Invalid or expired invitation.")

        user = invitation.user

        user.set_password(validated_data["password"])
        user.first_name = validated_data.get("first_name", "")
        user.last_name = validated_data.get("last_name", "")
        user.is_active = True  # ✅ Activate user upon registration
        user.save()

        invitation.delete()  # ✅ Remove invitation after successful registration

        return user

