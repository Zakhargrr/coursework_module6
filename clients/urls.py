from django.urls import path
from django.views.decorators.cache import cache_page

from clients.apps import ClientsConfig
from clients.views import ClientListView, ClientDetailView, ClientCreateView, ClientDeleteView, ClientUpdateView

app_name = ClientsConfig.name


urlpatterns = [
    path('clients-list', ClientListView.as_view(), name='clients_list'),
    path('client-details/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('create-client/', ClientCreateView.as_view(), name='create_client'),
    path('delete-client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('edit-client/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
]