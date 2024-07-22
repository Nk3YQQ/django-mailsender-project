from django import forms

from clients.models import Client
from mailing.models import Mailing


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
