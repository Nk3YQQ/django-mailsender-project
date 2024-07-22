from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog
from main.permissions import check_object_or_403


class BlogCreateView(LoginRequiredMixin, CreateView):
    """ Контроллер для создания блога """

    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        instance = form.save()
        instance.owner = self.request.user
        instance.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Создать статью', 'button': 'Создать'}
        return context_data


class BlogListView(LoginRequiredMixin, ListView):
    """ Контроллер для чтения блогов """

    model = Blog


class BlogDetailView(LoginRequiredMixin, DetailView):
    """ Контроллер для чтения одного блога """

    model = Blog

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)
        instance.view_count += 1
        instance.save()
        return instance


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """ Контроллер для обновления блога """

    model = Blog
    form_class = BlogForm
    permission_required = 'blog.change_blog'

    def get_object(self, queryset=None):
        instance = super().get_object(queryset)

        return check_object_or_403(instance, self.request.user)

    def get_success_url(self):
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['intent'] = {'title': 'Редактировать статью', 'button': 'Редактировать'}
        return context_data


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """ Контроллер для удаления блога """

    model = Blog
    success_url = reverse_lazy('blog:blog_list')
    permission_required = 'blog.delete_blog'
