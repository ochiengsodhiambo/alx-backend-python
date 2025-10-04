from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Only participants in a conversation can access it or its messages.
    """

    def has_object_permission(self, request, view, obj):
        # If object is a Conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If object is a Message (check its conversation)
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False

# chats/permissions.py
from rest_framework.permissions import BasePermission

class IsAuthenticatedOrAdminSafe(BasePermission):
    def has_permission(self, request, view):
        # allow access if it's the Django admin
        if request.path.startswith("/admin/"):
            return True
        return request.user and request.user.is_authenticated
        # allow access if user is authenticated 
        
