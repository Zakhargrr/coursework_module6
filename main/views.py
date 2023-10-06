from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from main.models import Mailing, MailingMessage
from main.services import scheduled_sending, ScheduledMailings
from main.forms import MailingForm, MailingMessageForm
from users.models import User


# Create your views here.


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(PermissionRequiredMixin, CreateView):
    model = Mailing
    permission_required = 'main.add_mailing'
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


class MailingDeleteView(PermissionRequiredMixin, DeleteView):
    model = Mailing
    permission_required = 'main.delete_mailing'
    success_url = reverse_lazy('main:mailings')


class MailingUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mailing
    permission_required = 'main.change_mailing'
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
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingMessageDeleteView(PermissionRequiredMixin, DeleteView):
    model = MailingMessage
    permission_required = 'main.delete_mailingmessage'
    success_url = reverse_lazy('main:mailing_messages')


class MailingMessageCreateView(PermissionRequiredMixin, CreateView):
    model = MailingMessage
    permission_required = 'main.add_mailingmessage'
    form_class = MailingMessageForm
    success_url = reverse_lazy('main:mailing_messages')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class MailingMessageUpdateView(PermissionRequiredMixin, UpdateView):
    model = MailingMessage
    permission_required = 'main.change_mailingmessage'
    form_class = MailingMessageForm
    success_url = reverse_lazy('main:mailing_messages')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MailingMessageDetailView(DetailView):
    model = MailingMessage


def stop_mailing(request, pk):
    if not request.user.is_staff:
        raise Http404
    user = Mailing.objects.get(pk=pk)
    user.status = "Завершена"
    user.save()
    return redirect(reverse('main:mailings'))
