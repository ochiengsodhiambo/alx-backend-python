# messaging/managers.py
from django.db import models

class MessageQuerySet(models.QuerySet):
    def unread_for_user(self, user):
        return self.filter(receiver=user, unread=True)
