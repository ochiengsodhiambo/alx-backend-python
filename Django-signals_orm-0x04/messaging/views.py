from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

from django.views.decorators.cache import cache_page


User = get_user_model()


# -------------------------
# Conversation ViewSet
# -------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by("-created_at")
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    @action(detail=True, methods=["post"], url_path="add-message")
    def add_message(self, request, pk=None):
        conversation = self.get_object()

        if request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                sender=request.user,
                conversation=conversation,
                receiver=request.data.get("receiver")  # receiver ID from request
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# Message ViewSet
# -------------------------
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation"]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user)


# -------------------------
# Edit a message
# -------------------------
@login_required
def edit_message(request, message_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    message = get_object_or_404(Message, pk=message_id)

    if not (request.user == message.sender or request.user.is_staff):
        return HttpResponseForbidden("You cannot edit this message.")

    new_content = request.POST.get("content", "").strip()
    if not new_content:
        return JsonResponse({"error": "No content provided"}, status=400)

    message.content = new_content
    message.save()

    return JsonResponse({
        "ok": True,
        "message_id": str(message.id),
        "new_content": new_content
    })


# -------------------------
# Delete a user
# -------------------------
@login_required
def delete_user_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    user = request.user
    user.delete()
    return JsonResponse({"deleted": True})


# -------------------------
# Simple health check
# -------------------------
def index(request):
    return HttpResponse("Chats app is working!")


# -------------------------
# Cached conversation view
# -------------------------
@cache_page(60)  # cache for 60 seconds
def conversation_list_view(request, conversation_id):
    convo = get_object_or_404(Conversation, pk=conversation_id)
    messages = (
        convo.messages
        .select_related("sender", "receiver")
        .prefetch_related("replies")
        .order_by("created_at")
    )
    return render(request, "chats/conversation.html", {
        "conversation": convo,
        "messages": messages
    })

