from django import forms

from mailsender_app.models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('created_at', 'ended_at', 'periodicity', 'client', 'message')

        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'}),
            'ended_at': forms.DateInput(attrs={'type': 'date'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'body')
