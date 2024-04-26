from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, ListView, DeleteView

from mailsender_app.forms import ClientForm, MailingForm, MessageForm
from mailsender_app.models import Client, Mailing, Message


class Index(TemplateView):
    template_name = 'mailsender_app/index.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailsender:main')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Создать клиента', 'button': 'Добавить клиента'}
        return context_data


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('mailsender:client_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Изменить клиента', 'button': 'Сохранить изменения'}
        return context_data


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailsender:main')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailsender:message_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Создать сообщение', 'button': 'Добавить сообщение'}
        return context_data


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailsender:main')

    def get_success_url(self):
        return reverse('mailsender:message_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Изменить сообщение', 'button': 'Сохранить изменения'}
        return context_data


class MessageDetailView(DetailView):
    model = Message


class MessageListView(ListView):
    model = Message


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailsender:message_list')


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailsender:main')


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing = self.object
        context_data['clients'] = list(getattr(client, 'email') for client in mailing.client.all())
        return context_data


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse('mailsender:message_detail', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailsender:mailing_list')
