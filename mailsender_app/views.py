from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic import DeleteView as BaseDeleteView
from django.views.generic import CreateView as BaseCreateView
from django.views.generic import ListView as BaseListView
from django.views.generic import UpdateView as BaseUpdateView
from django.views.generic import DetailView as BaseDetailView

from blog.models import Blog
from mailsender_app.forms import ClientForm, MailingForm, MessageForm
from mailsender_app.models import Client, Mailing, Message


class Index(TemplateView):
    template_name = 'mailsender_app/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['mailings'] = Mailing.objects.count()
        context_data['active_mailings'] = Mailing.objects.filter(is_active=True).count()
        context_data['clients'] = Client.objects.count()

        blogs = Blog.objects.order_by('?')[:3]

        context_data['blogs'] = blogs

        return context_data


class ListView(LoginRequiredMixin, BaseListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(owner_id=user) if not user.is_staff else queryset

        return queryset


class CreateView(LoginRequiredMixin, BaseCreateView):
    pass


class UpdateView(LoginRequiredMixin, BaseUpdateView):
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class DetailView(LoginRequiredMixin, BaseDetailView):
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_staff:
            raise Http404
        return self.object


class DeleteView(LoginRequiredMixin, BaseDeleteView):
    pass


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailsender:main')
    permission_required = 'mailsender_app.create_client'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Создать клиента', 'button': 'Добавить клиента'}
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'mailsender_app.change_client'

    def get_success_url(self):
        return reverse('mailsender:client_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Изменить клиента', 'button': 'Сохранить изменения'}
        return context_data


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailsender:main')
    permission_required = 'mailsender_app.delete_client'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailsender:message_list')
    permission_required = 'mailsender_app.create_message'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Создать сообщение', 'button': 'Добавить сообщение'}
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailsender:main')
    permission_required = 'mailsender_app.change_message'

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
    permission_required = 'mailsender_app.delete_message'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailsender:main')
    permission_required = 'mailsender_app.create_mailing'

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(is_active=True)
        queryset = queryset.filter(owner_id=user) if not user.is_staff else queryset

        return queryset


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
    permission_required = 'mailsender_app.change_mailing'

    def get_success_url(self):
        return reverse('mailsender:message_detail', args=[self.kwargs.get('pk')])


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailsender:mailing_list')
    permission_required = 'mailsender_app.delete_mailing'


@login_required
def deactivate_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.is_active:
        mailing.is_active = False
    else:
        mailing.is_active = True

    mailing.save()
    return redirect(reverse('mailsender:mailing_list'))
