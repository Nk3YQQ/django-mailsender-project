from django.contrib import admin

from mailsender_app.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'patronymic', 'email',)
