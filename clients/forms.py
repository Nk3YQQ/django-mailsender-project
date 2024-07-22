from django import forms

from clients.models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'surname', 'patronymic', 'email', 'comment')
