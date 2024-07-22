from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

from message.forms import MessageForm
from message.models import Message
from main.permissions import check_object_or_403


class MessageCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер для создания сообщения """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')
    permission_required = 'message.create_message'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Создать сообщение', 'button': 'Добавить сообщение'}
        return context_data

    def form_valid(self, form):
        instance = form.save()
        instance.owner = self.request.user
        instance.save()

        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    """ Контроллер для чтения сообщений """

    model = Message

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        queryset = queryset.filter(owner_id=user.pk) if not user.is_staff else queryset

        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер для чтения одного сообщения """

    model = Message

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)

        return check_object_or_403(instance, self.request.user)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер для обновления сообщения """

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:main')
    permission_required = 'message.change_message'

    def get_success_url(self):
        return reverse('message:message_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Изменить сообщение', 'button': 'Сохранить изменения'}
        return context_data

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)

        return check_object_or_403(instance, self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер для удаления сообщения """

    model = Message
    success_url = reverse_lazy('message:message_list')
    permission_required = 'message.delete_message'
