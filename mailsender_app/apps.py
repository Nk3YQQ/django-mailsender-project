from time import sleep

from django.apps import AppConfig


class MailsenderAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailsender_app'
    verbose_name = 'Рассылка'
