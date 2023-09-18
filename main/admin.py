from django.contrib import admin

from main.models import Client, MailingMessage, Mailing, Log


# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'second_name', 'patronymic', 'comment')


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'schedule', 'status', 'is_active', 'message')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'status', 'server_response')
