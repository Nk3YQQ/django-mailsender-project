from django import template

register = template.Library()


@register.filter()
def my_media(val):
    if val:
        return f'/media/{val}'
    return '/media/blog/not_found.png'
