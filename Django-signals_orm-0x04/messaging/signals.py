from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
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
        MessageHistory.objects.create(
            message=old,
            old_content=old.content,
            changed_by=getattr(instance, "editing_user", None) or old.sender,
        )
        instance.edited = True


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def cascade_delete_user_related(sender, instance, **kwargs):
    """
    When a User is deleted, cascade deletes messages and conversations.
    Clean up related notifications explicitly.
    """
    Notification.objects.filter(user=instance).delete()

