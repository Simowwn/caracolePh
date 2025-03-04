from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import UserInvitation
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class UserInvitationTests(APITestCase):
    def setUp(self):
        # Create an admin user (is_staff=True)
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            is_staff=True,
            is_active=True
        )
        
        # Create a regular user to be invited
        self.invitee = User.objects.create_user(
            email='invitee@test.com',
            password='testpass123',
            is_active=False
        )
        
        # Get token for admin user
        refresh = RefreshToken.for_user(self.admin_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Create a test invitation
        self.invitation = UserInvitation.objects.create(
            user=self.invitee
        )
        
        # URLs
        self.list_create_url = reverse('userinvitation-list')
        self.detail_url = reverse('userinvitation-detail', args=[str(self.invitation.id)])
        self.accept_url = reverse('userinvitation-accept', args=[str(self.invitation.id)])
        self.resend_url = reverse('userinvitation-resend', args=[str(self.invitation.id)])

    def test_create_invitation(self):
        """Test creating a new invitation"""
        new_user = User.objects.create_user(
            email='new@test.com',
            password='testpass123',
            is_active=False
        )
        
        data = {'email': new_user.email}
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserInvitation.objects.filter(user=new_user).exists())

    def test_list_invitations(self):
        """Test listing all invitations"""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should show our created invitation

    def test_retrieve_invitation(self):
        """Test retrieving a single invitation"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.invitee.id)

    def test_accept_invitation(self):
        """Test accepting an invitation"""
        response = self.client.post(self.accept_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh invitation from db
        self.invitation.refresh_from_db()
        self.assertTrue(self.invitation.is_invited)

    def test_accept_expired_invitation(self):
        """Test accepting an expired invitation"""
        # Set invitation to expired
        self.invitation.expires_at = timezone.now() - timedelta(days=1)
        self.invitation.save()
        
        response = self.client.post(self.accept_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('expired', response.data['error'])

    def test_accept_already_accepted_invitation(self):
        """Test accepting an already accepted invitation"""
        self.invitation.is_invited = True
        self.invitation.save()
        
        response = self.client.post(self.accept_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already accepted', response.data['error'])

    def test_resend_invitation(self):
        """Test resending an invitation"""
        response = self.client.post(self.resend_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('resent successfully', response.data['message'])

    def test_resend_expired_invitation(self):
        """Test resending an expired invitation"""
        self.invitation.expires_at = timezone.now() - timedelta(days=1)
        self.invitation.save()
        
        response = self.client.post(self.resend_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('expired', response.data['error'])

    def test_unauthorized_access(self):
        """Test unauthorized access to invitations"""
        # Remove credentials
        self.client.credentials()
        
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_staff_access(self):
        """Test non-staff user access to invitations"""
        # Create and login as non-staff user
        non_staff = User.objects.create_user(
            email='nonstaff@test.com',
            password='testpass123',
            is_active=True
        )
        refresh = RefreshToken.for_user(non_staff)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
