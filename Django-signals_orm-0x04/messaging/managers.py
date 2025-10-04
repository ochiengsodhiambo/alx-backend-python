# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager for unread message operations.
    Example: Message.unread.unread_for_user(user)
    """

    def get_queryset(self):
        # Only return messages marked as unread
        return super().get_queryset().filter(unread=True)

    def unread_for_user(self, user):
        """Return unread messages for a specific user"""
        return self.get_queryset().filter(receiver=user)
