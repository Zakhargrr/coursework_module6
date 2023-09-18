from django.db import models


# Create your models here.


class MailingMessage(models.Model):
    title = models.CharField(max_length=40, verbose_name='заголовок')
    body = models.TextField(verbose_name='тело письма')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'сообщение рассылки'
        verbose_name_plural = 'сообщения  рассылки'


SCHEDULE_CHOICES = [
    ("1D", "Раз в день"),
    ("1W", "Раз в неделю"),
    ("1M", "Раз в месяц"),
]


class Mailing(models.Model):
    datetime = models.DateTimeField(verbose_name='дата и время')
    schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, verbose_name='периодичность')
    status = models.CharField(max_length=20, default='Создана', verbose_name='статус')
    is_active = models.BooleanField(default=False, verbose_name='состояние скрипта')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, verbose_name='сообщение')

    def __str__(self):
        return f"{self.message}. {self.schedule} - {self.status}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Client(models.Model):
    email = models.EmailField(max_length=40, verbose_name='email')
    first_name = models.CharField(max_length=30, verbose_name='имя')
    second_name = models.CharField(max_length=30, verbose_name='фамилия')
    patronymic = models.CharField(max_length=30, verbose_name='отчество')
    comment = models.TextField(null=True, blank=True, verbose_name='комментарий')
    mailings = models.ManyToManyField(Mailing, verbose_name='рассылки')

    def __str__(self):
        return f"{self.first_name} {self.second_name} - {self.email}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    status = models.CharField(verbose_name="статус попытки")
    server_response = models.CharField(verbose_name='ответ сервера')

    def __str__(self):
        return f"{self.status} {self.server_response} {self.datetime}"

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
