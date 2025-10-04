from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # test view
    path("messages/edit/<int:message_id>/", views.edit_message, name="edit_message"),
    path("delete-account/", views.delete_user_view, name="delete_account"),
    path("conversations/<int:conversation_id>/", views.conversation_list_view, name="conversation_view"),

]

