from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Periodicity(models.TextChoices):
    DAILY = "Раз в день", "Раз в день"
    WEEKLY = "Раз в неделю", "Раз в неделю"
    MONTHLY = "Раз в месяц", "Раз в месяц"


class Status(models.TextChoices):
    FINISHED = "Завершена", "Завершена"
    CREATED = "Создана", "Создана"
    STARTED = "Запущена", "Запущена"


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)
    email = models.CharField(max_length=50, unique=True, verbose_name='Электронная почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Тело письма')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Mailing(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата первой отправки')
    ended_at = models.DateTimeField(verbose_name='Дата окончания отправки')

    periodicity = models.CharField(max_length=30, choices=Periodicity.choices, verbose_name='Периодичность')
    status = models.CharField(max_length=30, choices=Status.choices, verbose_name='Статус', default='Запущена')

    client = models.ManyToManyField(Client, related_name='mailing_list', verbose_name='Клиенты')
    message = models.ForeignKey(Message, on_delete=models.PROTECT, verbose_name='Сообщение')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='Активна')

    def __str__(self):
        return f'{self.message} - {self.periodicity} - {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Attempt(models.Model):
    SUCCESSFUL = 'successful'
    UNSUCCESSFUL = 'unsuccessful'
    STATUS = (
        (SUCCESSFUL, 'Успешно'),
        (UNSUCCESSFUL, 'Не успешно'),
    )

    attempt_time = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата последней попытки')
    status = models.CharField(max_length=30, choices=STATUS, verbose_name='Статус')
    server_response = models.CharField(max_length=100, verbose_name='Ответ сервера')

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Попытка')
    client = models.ForeignKey(Client, verbose_name='клиент', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.attempt_time} - {self.status} - {self.server_response[:50]}'

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
