from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from main.models import Mailing, MailingMessage
from main.services import scheduled_sending, ScheduledMailings
from main.forms import MailingForm, MailingMessageForm


# Create your views here.


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailings')

    def get_form_kwargs(self):
        kwargs = super(MailingCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Новая запись"
        return context_data

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

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
    form_class = MailingForm
    success_url = reverse_lazy('main:mailings')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MailingMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage

    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user
        )


class MailingMessageDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('main:mailing_messages')


class MailingMessageCreateView(CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('main:mailing_messages')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingMessageUpdateView(UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('main:mailing_messages')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MailingMessageDetailView(DetailView):
    model = MailingMessage
