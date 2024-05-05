from django import forms

from mailsender_app.models import Client, Mailing, Message


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'surname', 'patronymic', 'email', 'comment')


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('created_at', 'ended_at', 'periodicity', 'client', 'message')

        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'}),
            'ended_at': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        if owner:
            self.fields['client'] = forms.ModelMultipleChoiceField(
                label='Клиенты',
                queryset=Client.objects.filter(owner=owner),
                widget=forms.CheckboxSelectMultiple
            )


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'body')
