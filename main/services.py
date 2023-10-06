from smtplib import SMTPException

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from datetime import datetime

from main.models import Mailing, Log


class ScheduledMailings:
    is_active = False
    daily_scheduler = BackgroundScheduler()
    weekly_scheduler = BackgroundScheduler()
    monthly_scheduler = BackgroundScheduler()
    checkup_scheduler = BackgroundScheduler()

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

    @classmethod
    def scheduled_checkup(cls):
        state = 'checkup'
        cls.checkup_scheduler.add_job(send_clients_email, 'interval', minutes=10, args=[state])
        cls.checkup_scheduler.start()


def scheduled_sending():
    scheduler = BackgroundScheduler()
    state = 'created_mailing'
    scheduler.add_job(send_clients_email, 'interval', seconds=3, args=[state, scheduler])
    scheduler.start()


def send_email_in_correct_time(mailing_item):
    if datetime.now() >= mailing_item.datetime_start:
        if datetime.now() < mailing_item.datetime_finish:
            if mailing_item.status != "Завершена":
                mailing_item.status = "Активна"
                mailing_item.save()
                clients = mailing_item.clients.all()
                clients_arr = [client.email for client in clients]

                try:
                    send_mail(
                        f'{mailing_item.message.title}',
                        f'{mailing_item.message.body}',
                        'noreply@oscarbot.ru',
                        clients_arr
                    )
                    Log.objects.create(datetime=datetime.now, status='Успешно', message=mailing_item.message)
                except SMTPException as err:
                    Log.objects.create(datetime=datetime.now, status='Ошибка отправки', server_response=err,
                                       message=mailing_item.message)

                if not mailing_item.is_sent_by_schedule:
                    mailing_item.is_sent_by_schedule = True
                    mailing_item.save()
        else:
            mailing_item.status = "Завершена"
            mailing_item.save()


def send_clients_email(state, scheduler=None):
    if state == 'created_mailing':

        mailing_items_arr = [Mailing.objects.latest('pk')]
        # print(datetime.utcnow(), datetime.now(), mailing_items_arr[0].datetime_start)
        scheduler.pause()
    elif state == 'daily_mailing':
        mailing_items_arr = Mailing.objects.filter(schedule="1D")
    elif state == 'weekly_mailing':
        mailing_items_arr = Mailing.objects.filter(schedule="1W")
    elif state == 'monthly_mailing':
        mailing_items_arr = Mailing.objects.filter(schedule="1M")
    elif state == 'checkup':
        mailing_items_arr = Mailing.objects.all()
    else:
        return
    for mailing_item in mailing_items_arr:
        # print(mailing_item, mailing_item.is_sent_by_schedule, type(mailing_item.is_sent_by_schedule))
        if state == 'checkup':
            if not mailing_item.is_sent_by_schedule:
                if mailing_item.status != "Завершена":
                    send_email_in_correct_time(mailing_item)
            if datetime.now() > mailing_item.datetime_finish:
                mailing_item.status = "Завершена"
                mailing_item.save()
        else:
            if mailing_item.status != "Завершена":
                send_email_in_correct_time(mailing_item)
