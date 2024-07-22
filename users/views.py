from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView

from users.forms import RegisterForm
from users.models import User


class LoginView(BaseLoginView):
    """ Контроллер для входа в аккаунт """

    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Вход', 'button': 'Войти'}
        return context_data


class LogoutView(BaseLogoutView):
    """ Контроллер для выхода из аккаунта """

    pass


class RegisterView(CreateView):
    """ Контроллер для регистрации пользователя """

    model = User
    form_class = RegisterForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Регистрация', 'button': 'Зарегистрироваться'}
        return context_data


class UserListView(ListView):
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)

        return queryset


class UserDetailView(DetailView):
    """ Контроллер для чтения пользователя """

    model = User


@login_required
def deactivate_user(request, pk):
    """ Контроллер для деактивации пользователя """

    user = get_object_or_404(User, pk=pk)

    if user.is_active:
        user.is_active = False

    else:
        user.is_active = True

    user.save()

    return redirect(reverse('users:user_list'))
