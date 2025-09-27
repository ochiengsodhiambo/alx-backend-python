
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - User must be authenticated
    - User must be a participant in the conversation
    - Restricts unsafe methods (PUT, PATCH, DELETE) to participants only
    """

    def has_permission(self, request, view):
        # Global check: user must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Double-check authentication at object level
        if not user or not user.is_authenticated:
            return False

        # Conversation object
        if hasattr(obj, "participants"):
            if user not in obj.participants.all():
                raise PermissionDenied(detail="You are not a participant in this conversation.", code="HTTP_403_FORBIDDEN")
            return True

        # Message object
        if hasattr(obj, "conversation"):
            if user not in obj.conversation.participants.all():
                raise PermissionDenied(detail="You are not a participant in this conversation.", code="HTTP_403_FORBIDDEN")

            # Restrict unsafe methods
            if request.method in ["PUT", "PATCH", "DELETE"] and user not in obj.conversation.participants.all():
                raise PermissionDenied(detail="You cannot modify this message.", code="HTTP_403_FORBIDDEN")
            return True

        return False
