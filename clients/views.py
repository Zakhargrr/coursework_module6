from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from clients.models import Client


# Create your views here.

class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('second_name', 'first_name', 'patronymic', 'email', 'comment')
    success_url = reverse_lazy('clients:clients_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Новый клиент"
        return context_data


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('clients:clients_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('second_name', 'first_name', 'patronymic', 'email', 'comment')
    success_url = reverse_lazy('clients:clients_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Изменить клиента"
        return context_data
