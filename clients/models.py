from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """ Модель для клиента """

    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)
    email = models.CharField(max_length=50, unique=True, verbose_name='Электронная почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
