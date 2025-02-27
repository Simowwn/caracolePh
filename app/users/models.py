import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ✅ UUID primary key
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]  # ✅ Fix field names

    def __str__(self):
        return self.email
