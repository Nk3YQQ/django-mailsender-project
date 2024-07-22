from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import (MailingCreateView, MailingListView, MailingDetailView, MailingUpdateView, MailingDeleteView,
                           deactivate_mailing)

app_name = MailingConfig.name

urlpatterns = [
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('activity/<int:pk>/', deactivate_mailing, name='mailing_activity')
]
