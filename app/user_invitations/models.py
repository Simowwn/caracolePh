import uuid
from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class UserInvitation(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # email = models.EmailField(unique=True)  # ✅ Store email instead of FK to User
    # token = models.UUIDField(default=uuid.uuid4, unique=True)
    # is_invited = models.BooleanField(default=False)
    # expires_at = models.DateTimeField(default=lambda: now() + timedelta(days=7))  # Expires in 7 days
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f"Invitation for {self.email} - {'Expired' if self.is_expired() else 'Active'}"
