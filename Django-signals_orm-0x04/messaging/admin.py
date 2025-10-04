from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message, MessageHistory, Notification


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone_number", "role")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name", "last_name", "phone_number", "role",
                "password1", "password2", "is_staff", "is_active"
            ),
        }),
    )


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
    filter_horizontal = ("participants",)


# Inline for message history
class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ("old_content", "changed_at", "changed_by")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "receiver", "content", "created_at", "edited")
    list_filter = ("edited", "created_at")
    search_fields = ("content",)
    inlines = [MessageHistoryInline]   # Attach history inline


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "old_content", "changed_at", "changed_by")
    list_filter = ("changed_at",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "created_at", "is_read")
    list_filter = ("is_read", "created_at")

