from django.http import HttpResponseForbidden


def check_object_or_403(instance, current_user):
    """ Проверка доступности страницы для пользователя """

    if instance.owner != current_user and not current_user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")

    return instance
