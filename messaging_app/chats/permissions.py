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
