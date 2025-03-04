from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserInvitation
from .serializers import UserInvitationSerializer

class UserInvitationViewSet(viewsets.ModelViewSet):
    queryset = UserInvitation.objects.all()
    serializer_class = UserInvitationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
    
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
