from django.contrib import admin

from main.models import MailingMessage, Mailing, Log


# Register your models here.


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'datetime_start', 'datetime_finish', 'schedule', 'status', 'is_active',)
    list_filter = ('status', 'is_active', 'clients')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'status', 'server_response')
