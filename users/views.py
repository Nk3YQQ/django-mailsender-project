from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from users.forms import RegisterForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Вход', 'button': 'Войти'}
        return context_data


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
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
