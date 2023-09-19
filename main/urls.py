from django.urls import path

from main.apps import MainConfig
from main.views import MailingListView, MailingDetailView, MailingCreateView

app_name = MainConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailings'),
    path('mailing-details/<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('create-details', MailingCreateView.as_view(), name='create_mailing')
]
