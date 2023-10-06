from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from clients.forms import ClientForm
from clients.models import Client


# Create your views here.

class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    permission_required = 'clients.add_client'
    success_url = reverse_lazy('clients:clients_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Новый клиент"
        return context_data

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ClientDeleteView(PermissionRequiredMixin, DeleteView):
    model = Client
    permission_required = 'clients.delete_client'
    success_url = reverse_lazy('clients:clients_list')


class ClientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Client
    permission_required = 'clients.change_client'
    form_class = ClientForm
    success_url = reverse_lazy('clients:clients_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = "Изменить клиента"
        return context_data
