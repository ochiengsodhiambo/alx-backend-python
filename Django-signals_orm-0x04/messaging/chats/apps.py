from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chats'
    
    def ready(self):
        # Import signals so they are registered
        import chats.signals  # noqa
