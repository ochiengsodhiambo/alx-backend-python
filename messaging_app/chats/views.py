from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .auth import IsParticipantOfConversation   # pushing to auth.py


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversations:
    - Only authenticated users who are participants will access
    - Supports custom action to add messages into a conversation
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only return conversations where current user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        """Custom action: POST /api/conversations/{id}/add_message/"""
        conversation = self.get_object()

        if request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Messages:
    - Authenticated users only
    - Only participants of the conversation can see or create messages
    - Supports filtering & pagination
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    
    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)


# Quick health check endpoint
from django.http import HttpResponse

def index(request):
    return HttpResponse("Chats app is working!")
