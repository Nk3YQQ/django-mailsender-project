from django.views.generic import TemplateView

from blog.models import Blog
from clients.models import Client
from mailing.models import Mailing


class Index(TemplateView):
    """ Контроллер, отвечающий за вывод главной страницы """

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['mailings'] = Mailing.objects.count()
        context_data['active_mailings'] = Mailing.objects.filter(is_active=True).count()
        context_data['clients'] = Client.objects.count()

        blogs = Blog.objects.order_by('?')[:3]

        context_data['blogs'] = blogs

        return context_data
