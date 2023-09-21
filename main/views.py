from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from main.models import Mailing, MailingMessage


# Create your views here.

class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('message', 'datetime_start', 'datetime_finish', 'schedule', 'clients')
    success_url = reverse_lazy('main:mailings')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Новая запись"
        return context_data


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    fields = ('title', 'body')
    success_url = reverse_lazy('main:create_mailing')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Создать сообщение"
        return context_data


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
