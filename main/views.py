from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from main.models import Mailing


# Create your views here.

class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    fields = ('message', 'datetime_start', 'datetime_finish', 'schedule')
    success_url = reverse_lazy('main:mailings')
