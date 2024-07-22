from django.contrib import admin

from mailsender_app.models import Client, Message, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'patronymic', 'email', 'owner')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'owner')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'ended_at', 'periodicity', 'status', 'owner')
