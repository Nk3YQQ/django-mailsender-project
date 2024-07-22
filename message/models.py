from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    """ Модель для сообщений """

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Тело письма')

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
