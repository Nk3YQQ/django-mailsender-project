from django.contrib import admin

from message.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'owner')
