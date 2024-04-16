from django import forms

from mailsender_app.models import Client


class ClientForm(forms.Form):
    class Meta:
        model = Client
        fields = '__all__'
