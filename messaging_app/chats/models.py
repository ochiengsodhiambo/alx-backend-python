import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# 1. Custom User model
class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[("guest", "Guest"), ("host", "Host"), ("admin", "Admin")],
        default="guest",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Keep username for login, and also keep email unique
    email = models.EmailField(unique=True)

    #  Use the default USERNAME_FIELD ("username") → no change
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return f"{self.username} ({self.email}, {self.role})"


# 2. Conversation model
class Conversation(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# 3. Message model
class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    message_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  
    def __str__(self):
        return f"Message {self.id} from {self.sender.username}"

