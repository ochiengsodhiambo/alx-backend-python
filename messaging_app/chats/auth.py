from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission: Only participants of a conversation can view, create,
    update, or delete its messages.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False
