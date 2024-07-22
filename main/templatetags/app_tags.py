from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def get_patronymic_or_not(val):
    if val:
        return val
    return 'Нет'


@register.filter
def is_moderator(user):
    moderator_group = Group.objects.get(name='Модератор')
    return moderator_group in user.groups.all()


@register.filter
def my_media(val):
    if val:
        return f'/media/{val}'
    return '/media/blog/not_found.png'
