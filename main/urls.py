from django.urls import path

from main.apps import MainConfig
from main.views import MailingListView, MailingDetailView, MailingCreateView, MailingDeleteView, MailingUpdateView, \
    MailingMessageCreateView

app_name = MainConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailings'),
    path('mailing-details/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('create-mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('delete-mailing/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('edit-mailing/<int:pk>/', MailingUpdateView.as_view(), name='edit_mailing'),
    path('create-mailing-message/', MailingMessageCreateView.as_view(), name='create_mailing_message')
]
