from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from main.models import Mailing, MailingMessage
from main.services import scheduled_sending, ScheduledMailings
from main.templates.main.forms import MailingForm


# Create your views here.

class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailings')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Новая запись"
        return context_data

    def form_valid(self, form):
        if not ScheduledMailings.is_active:
            ScheduledMailings.send_daily_mailings()
            ScheduledMailings.send_weekly_mailings()
            ScheduledMailings.send_monthly_mailings()
            ScheduledMailings.scheduled_checkup()
            ScheduledMailings.is_active = True
        scheduled_sending()

        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailings')


class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ('message', 'datetime_start', 'datetime_finish', 'schedule', 'clients')
    success_url = reverse_lazy('main:mailings')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Изменить запись"
        return context_data


class MailingMessageListView(ListView):
    model = MailingMessage


class MailingMessageDetailView(DetailView):
    model = Mailing


class MailingMessageDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailings')


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    fields = ('title', 'body')
    success_url = reverse_lazy('main:mailing_messages')
