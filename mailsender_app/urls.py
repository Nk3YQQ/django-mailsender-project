from django.urls import path
from django.views.decorators.cache import cache_page

from mailsender_app.apps import MailsenderAppConfig
from mailsender_app.views import ClientCreateView, Index, ClientDetailView, ClientUpdateView, ClientListView, \
    ClientDeleteView, MailingCreateView, MailingListView, MessageCreateView, MessageUpdateView, MessageDetailView, \
    MessageListView, MessageDeleteView, MailingDetailView, MailingUpdateView, MailingDeleteView, deactivate_mailing

app_name = MailsenderAppConfig.name

urlpatterns = [
    path('', cache_page(60)(Index.as_view()), name='main'),

    # Clients
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    # Mailing
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/edit/<int:pk>', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing/delete/<int:pk>', MailingDeleteView.as_view(), name='mailing_delete'),
    path('activity/<int:pk>', deactivate_mailing, name='activity'),

    # Message
    path('message/create', MessageCreateView.as_view(), name='message_create'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('message/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
