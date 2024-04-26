# Generated by Django 5.0.4 on 2024-04-24 19:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=100, null=True, verbose_name='Отчество')),
                ('email', models.CharField(max_length=50, unique=True, verbose_name='Электронная почта')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('body', models.TextField(verbose_name='Тело письма')),
            ],
            options={
                'verbose_name': 'письмо',
                'verbose_name_plural': 'письма',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Дата первой отправки')),
                ('ended_at', models.DateTimeField(verbose_name='Дата окончания отправки')),
                ('periodicity', models.CharField(choices=[('daily', 'Раз в день'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=30, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('finished', 'Завершена'), ('created', 'Создана'), ('started', 'Запущена')], max_length=30, verbose_name='Статус')),
                ('client', models.ManyToManyField(related_name='mailing_list', to='mailsender_app.client', verbose_name='Клиенты')),
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='mailsender_app.message', verbose_name='Сообщение')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата последней попытки')),
                ('status', models.CharField(choices=[('successful', 'Успешно'), ('unsuccessful', 'Не успешно')], max_length=30, verbose_name='Статус')),
                ('server_response', models.CharField(max_length=100, verbose_name='Ответ сервера')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailsender_app.client', verbose_name='клиент')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailsender_app.mailing', verbose_name='Попытка')),
            ],
            options={
                'verbose_name': 'попытка',
                'verbose_name_plural': 'попытки',
            },
        ),
    ]
