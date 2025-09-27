from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .auth import IsParticipantOfConversation
from rest_framework.status import HTTP_403_FORBIDDEN   # ✅ Explicit import


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id"] # Filter by "conversation_id"

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        conversation = self.get_object()

        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=HTTP_403_FORBIDDEN,
            )

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation", "sender"]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        conversation = serializer.instance.conversation
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=HTTP_403_FORBIDDEN,
            )
        serializer.save()

    def perform_destroy(self, instance):
        conversation = instance.conversation
        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=HTTP_403_FORBIDDEN,
            )
        instance.delete()


# Health check
def index(request):
    return HttpResponse("Chats app is working!")
