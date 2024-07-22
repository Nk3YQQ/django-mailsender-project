from django.urls import path

from message.apps import MessagesConfig
from message.views import MessageCreateView, MessageListView, MessageUpdateView, MessageDetailView, MessageDeleteView

app_name = MessagesConfig.name

urlpatterns = [
    path('create/', MessageCreateView.as_view(), name='message_create'),
    path('', MessageListView.as_view(), name='message_list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
