import uuid
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings  # Add this import
from django.utils import timezone

def default_expiry():
    return now() + timedelta(days=7)

class UserInvitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invitations")
    is_invited = models.BooleanField(default=False)
    expires_at = models.DateTimeField(default=default_expiry)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f"Invitation for {self.user.email} - {'Expired' if self.is_expired() else 'Active'}"