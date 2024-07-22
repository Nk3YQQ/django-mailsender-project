from datetime import timedelta

from django.contrib.auth.hashers import make_password

from users.models import User


def choose_periodicity(mailing):
    if mailing.periodicity == 'Раз в день':
        mailing.created_at += timedelta(days=1)
    elif mailing.periodicity == 'Раз в неделю':
        mailing.created_at += timedelta(weeks=1)
    elif mailing.periodicity == 'Раз в месяц':
        mailing.created_at += timedelta(days=30)

    mailing.save()


def update_mailing_status(mailing, current_datetime):
    if current_datetime > mailing.ended_at:
        mailing.status = 'Завершена'
    elif current_datetime < mailing.created_at:
        mailing.status = 'Создана'
    else:
        mailing.status = 'Запущена'

    mailing.save()


def create_user():
    return User.objects.create(
        first_name='Test',
        last_name='Testov',
        email='test@mail.ru',
        password=make_password('123qwe456rty')
    )
