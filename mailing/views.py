from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing.forms import MailingForm
from mailing.models import Mailing
from main.permissions import check_object_or_403


class MailingCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер для создания рассылки """

    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_create')
    permission_required = 'mailsender.create_mailing'

    def form_valid(self, form):
        instance = form.save()
        instance.owner = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs


class MailingListView(LoginRequiredMixin, ListView):
    """ Контроллер для чтения рассылок """

    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(is_active=True)
        queryset = queryset.filter(owner_id=user.pk) if not user.is_staff else queryset

        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер для чтения одной рассылки """

    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing = self.object
        context_data['clients'] = list(getattr(client, 'email') for client in mailing.client.all())
        return context_data

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)

        return check_object_or_403(instance, self.request.user)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер для обновления рассылки """

    model = Mailing
    form_class = MailingForm
    permission_required = 'mailing.change_mailing'

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.kwargs.get('pk')])

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)

        return check_object_or_403(instance, self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер для удаления рассылки """

    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.delete_mailing'


@login_required
def deactivate_mailing(request, pk):
    """ Контроллер для деактивации рассылки """

    mailing = get_object_or_404(Mailing, pk=pk)

    if mailing.is_active:
        mailing.is_active = False

    else:
        mailing.is_active = True

    mailing.save()

    return redirect(reverse('mailsender:mailing_list'))
