from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from datetime import datetime

from main.models import Mailing


class ScheduledMailings:
    is_active = False
    daily_scheduler = BackgroundScheduler()
    weekly_scheduler = BackgroundScheduler()
    monthly_scheduler = BackgroundScheduler()

    @classmethod
    def send_daily_mailings(cls):
        state = 'daily_mailing'
        cls.daily_scheduler.add_job(send_clients_email, 'interval', days=1, args=[state])
        cls.daily_scheduler.start()

    @classmethod
    def send_weekly_mailings(cls):
        state = 'weekly_mailing'
        cls.weekly_scheduler.add_job(send_clients_email, 'interval', weeks=1, args=[state])
        cls.weekly_scheduler.start()

    @classmethod
    def send_monthly_mailings(cls):
        state = 'monthly_mailing'
        cls.monthly_scheduler.add_job(send_clients_email, 'interval', weeks=4, args=[state])
        cls.monthly_scheduler.start()


def scheduled_sending():
    scheduler = BackgroundScheduler()
    state = 'created_mailing'
    scheduler.add_job(send_clients_email, 'interval', seconds=3, args=[state, scheduler])
    scheduler.start()


def send_clients_email(state, scheduler=None):
    if state == 'created_mailing':
        mailing_items_arr = [Mailing.objects.latest('pk')]
        scheduler.pause()
    elif state == 'daily_mailing':
        mailing_items_arr = Mailing.objects.filter(schedule="1D")
    elif state == 'weekly_mailing':
        mailing_items_arr = Mailing.objects.filter(schedule="1W")
    elif state == 'monthly_mailing':
        mailing_items_arr = Mailing.objects.filter(schedule="1M")
    else:
        return
    for mailing_item in mailing_items_arr:
        if datetime.utcnow() >= mailing_item.datetime_start:
            if datetime.utcnow() < mailing_item.datetime_finish:
                mailing_item.status = "Активна"
                mailing_item.save()
                clients = mailing_item.clients.all()
                clients_arr = [client.email for client in clients]
                send_mail(
                    f'{mailing_item.message.title}',
                    f'{mailing_item.message.body}',
                    'noreply@oscarbot.ru',
                    clients_arr
                )
            else:
                mailing_item.status = "Завершена"
                mailing_item.save()
