from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from clients.forms import ClientForm
from clients.models import Client
from main.permissions import check_object_or_403


class ClientCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер для создания клиента """

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:client_list')
    permission_required = 'clients.create_client'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Создать клиента', 'button': 'Добавить клиента'}
        return context_data

    def form_valid(self, form):
        instance = form.save()
        instance.owner = self.request.user
        instance.save()

        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """ Контроллер для чтения клиентов """

    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user

        queryset = queryset.filter(owner_id=user.pk) if not user.is_staff else queryset

        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер для чтения одного клиента """

    model = Client

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)

        return check_object_or_403(instance, self.request.user)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер для обновления клиента """

    model = Client
    form_class = ClientForm
    permission_required = 'clients.change_client'

    def get_success_url(self):
        return reverse('clients:client_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Изменить клиента', 'button': 'Сохранить изменения'}
        return context_data

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)

        return check_object_or_403(instance, self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер для удаления клиента """

    model = Client
    success_url = reverse_lazy('clients:client_list')
    permission_required = 'clients.delete_client'
