import uuid
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
import random
import string

def default_expiry():
    return now() + timedelta(days=7)

def generate_token(length=6):
    """Generate a random token with letters and numbers"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class UserInvitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invitations")
    token = models.CharField(max_length=10, unique=True, blank=True)
    is_invited = models.BooleanField(default=False)
    expires_at = models.DateTimeField(default=default_expiry)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.token:
            # Generate a unique token
            while True:
                token = generate_token()
                if not UserInvitation.objects.filter(token=token).exists():
                    self.token = token
                    break
        super().save(*args, **kwargs)

    def is_expired(self):
        return now() > self.expires_at

    def __str__(self):
        return f"Invitation for {self.user.email} - {'Expired' if self.is_expired() else 'Active'}"