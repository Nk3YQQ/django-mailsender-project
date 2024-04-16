from django.urls import path

from mailsender_app.apps import MailsenderAppConfig
from mailsender_app.views import ClientCreateView, Index, ClientDetailView, ClientUpdateView

app_name = MailsenderAppConfig.name

urlpatterns = [
    path('', Index.as_view(), name='main'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
]
