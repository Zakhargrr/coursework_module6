from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import MailingListView, MailingDetailView, MailingCreateView, MailingDeleteView, MailingUpdateView, \
    MailingMessageCreateView, MailingMessageListView, MailingMessageDetailView, MailingMessageUpdateView, \
    MailingMessageDeleteView, stop_mailing, main_page

app_name = MainConfig.name

urlpatterns = [
    path('', main_page, name='main_page'),
    path('mailings', MailingListView.as_view(), name='mailings'),
    path('mailing-details/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('create-mailing/', MailingCreateView.as_view(), name='create_mailing'),
    path('delete-mailing/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),
    path('edit-mailing/<int:pk>/', MailingUpdateView.as_view(), name='edit_mailing'),
    path('create-mailing-message/', MailingMessageCreateView.as_view(), name='create_mailing_message'),
    path('mailing-messages/', MailingMessageListView.as_view(), name='mailing_messages'),
    path('mailing-message-detail/<int:pk>/', cache_page(60)(MailingMessageDetailView.as_view()), name='mailing_message_detail'),
    path('edit-mailing-message/<int:pk>/', MailingMessageUpdateView.as_view(), name='edit_mailing_message'),
    path('delete-mailing-message/<int:pk>/', MailingMessageDeleteView.as_view(), name='delete_mailing_message'),
    path('stop-mailing/<int:pk>/', stop_mailing, name='stop_mailing'),
]
