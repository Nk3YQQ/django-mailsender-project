from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Periodicity(models.TextChoices):
    DAILY = "Раз в день", "Раз в день"
    WEEKLY = "Раз в неделю", "Раз в неделю"
    MONTHLY = "Раз в месяц", "Раз в месяц"


class Status(models.TextChoices):
    FINISHED = "Завершена", "Завершена"
    CREATED = "Создана", "Создана"
    STARTED = "Запущена", "Запущена"


class Mailing(models.Model):
    """ Модель для рассылок """

    created_at = models.DateTimeField(verbose_name='Дата первой отправки')
    ended_at = models.DateTimeField(verbose_name='Дата окончания отправки')

    periodicity = models.CharField(max_length=30, choices=Periodicity.choices, verbose_name='Периодичность')
    status = models.CharField(max_length=30, choices=Status.choices, verbose_name='Статус', default='Запущена')

    client = models.ManyToManyField('clients.Client', related_name='mailing_list', verbose_name='Клиенты')
    message = models.ForeignKey('message.Message', on_delete=models.PROTECT, verbose_name='Сообщение')

    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f'{self.message} - {self.periodicity} - {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Attempt(models.Model):
    """ Модель для попытки """

    SUCCESSFUL = 'successful'
    UNSUCCESSFUL = 'unsuccessful'
    STATUS = (
        (SUCCESSFUL, 'Успешно'),
        (UNSUCCESSFUL, 'Не успешно'),
    )

    attempt_time = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата последней попытки')
    status = models.CharField(max_length=30, choices=STATUS, verbose_name='Статус')
    server_response = models.CharField(max_length=100, verbose_name='Ответ сервера')

    mailing = models.ForeignKey('mailing.Mailing', on_delete=models.CASCADE, verbose_name='Попытка')
    client = models.ForeignKey('clients.Client', verbose_name='клиент', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.attempt_time} - {self.status} - {self.server_response[:50]}'

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
