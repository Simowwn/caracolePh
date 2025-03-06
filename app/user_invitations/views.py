from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserInvitation
from .serializers import UserInvitationSerializer
from rest_framework.views import APIView  
from .serializers import InvitedRegistrationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveAPIView 



class UserInvitationViewSet(viewsets.ModelViewSet):
    queryset = UserInvitation.objects.all()
    serializer_class = UserInvitationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        invitation = serializer.save()
    
    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        invitation = self.get_object()
        if invitation.is_expired():
            return Response(
                {"error": "Invitation has expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message":"Invitation resent successfully"})
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        invitation = self.get_object()
        if invitation.is_expired():
            return Response(
                {"error": "Invitation has expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if invitation.is_invited:
            return Response(
                {"error": "Invitation already accepted"},
                status=status.HTTP_400_BAD_REQUEST
            )
        invitation.is_invited = True
        invitation.save()
        return Response({"message": "Invitation accepted successfully"})
# Create your views here.


 # Instead of APIView

class InvitedUserRegistrationView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = InvitedRegistrationSerializer

    def get(self, request, token):
        invitation = get_object_or_404(UserInvitation, token=token)  # ✅ Remove is_invited=True filter
        user = invitation.user

        if user.is_active:
            return Response({"error": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, token):
        """Register the user if the token is valid."""
        invitation = get_object_or_404(UserInvitation, token=token, is_invited=False)  
        user = invitation.user  # Get the associated user

        if user.is_active:
            return Response({"error": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Create a mutable copy of request data and add email automatically
        data = request.data.copy()
        data["email"] = user.email  # Set email from UserInvitation

        serializer = InvitedRegistrationSerializer(data=data, context={"token": token})

        if serializer.is_valid():
            user.set_password(serializer.validated_data["password"])
            user.first_name = serializer.validated_data.get("first_name", "")
            user.last_name = serializer.validated_data.get("last_name", "")
            user.is_active = True  # ✅ Activate the user
            user.save()

            invitation.is_invited = True  # ✅ Mark the invitation as used
            invitation.save()

            return Response({"message": "Registration successful", "user_id": user.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

