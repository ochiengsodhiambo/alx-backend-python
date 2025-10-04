from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings

from .models import Message, Notification, MessageHistory, User


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance: Message, created, **kwargs):
    """
    When a new message is created, create a Notification for the receiver.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
        )

        # Example use of Message.objects.filter(...) — optional enhancement:
        # Mark all unread messages from this conversation as seen
        Message.objects.filter(
            conversation=instance.conversation,
            receiver=instance.receiver,
            edited=False
        ).exclude(pk=instance.pk).update(edited=True)


@receiver(pre_save, sender=Message)
def save_message_history_before_edit(sender, instance: Message, **kwargs):
    """
    Before a message is saved, if content changes, archive old content in MessageHistory.
    """
    if not instance.pk:
        return  # new message, nothing to archive

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old.content != instance.content:
        # Log the history of the old content
        MessageHistory.objects.create(
            message=old,
            old_content=old.content,
            changed_by=getattr(instance, "editing_user", None) or old.sender,
        )

        # Mark message as edited with timestamp
        instance.edited = True
        instance.edited_at = timezone.now()
        instance.edited_by = getattr(instance, "editing_user", None) or old.sender


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def cascade_delete_user_related(sender, instance, **kwargs):
    """
    When a User is deleted, cascade deletes messages and conversations.
    Clean up related notifications explicitly.
    """
    Notification.objects.filter(user=instance).delete()
