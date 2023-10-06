from django.conf import settings
from django.db import models

# Create your models here.


class Client(models.Model):
    email = models.EmailField(max_length=40, verbose_name='email', unique=True)
    second_name = models.CharField(max_length=30, verbose_name='фамилия')
    first_name = models.CharField(max_length=30, verbose_name='имя')
    patronymic = models.CharField(max_length=30, verbose_name='отчество')
    comment = models.TextField(null=True, blank=True, verbose_name='комментарий')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='владелец')

    def __str__(self):
        return f"{self.first_name} {self.second_name} - {self.email}"

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
