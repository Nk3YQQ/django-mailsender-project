from django import forms

from message.models import Message


class MessageForm(forms.ModelForm):
    """ Форма для сообщений """

    class Meta:
        model = Message
        fields = ('title', 'body')
