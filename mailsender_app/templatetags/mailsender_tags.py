from django import template

register = template.Library()


@register.filter()
def get_patronymic_or_not(val):
    if val:
        return val
    return 'Нет'
