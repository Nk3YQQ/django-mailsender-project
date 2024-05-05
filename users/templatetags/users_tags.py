from django import template

register = template.Library()


@register.filter()
def login_or_register(val):
    if val == 'registration':
        return
