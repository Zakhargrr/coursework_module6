from django.db import models


# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=30, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='previews/', verbose_name='изображение', null=True, blank=True)
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')

    def __str__(self):
        return f'{self.title}. Создано: {self.published_at}. Просмотров: {self.views_count}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
