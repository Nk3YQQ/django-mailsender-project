import datetime

from django.test import TestCase
from django.utils import timezone

from mailsender_app.models import Client, Message, Mailing
from mailsender_app.services import create_user


class MailingTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mailing_id = 1

    @classmethod
    def setUpTestData(cls):
        created_at = timezone.now()
        ended_at = created_at + datetime.timedelta(weeks=1)
        user = create_user()
        client = Client.objects.create(name='Client', surname='Clientov', email='client@mail.ru')
        message = Message.objects.create(title='Test', body='Hello, Django!')

        mailing = Mailing.objects.create(
            created_at=created_at,
            ended_at=ended_at,
            periodicity='Раз в неделю',
            message=message,
            owner=user
        )

        mailing.client.add(client)
        mailing.save()

    def login_and_go_to_mailing_page(self):
        self.client.login(email='test@mail.ru', password='123qwe456rty')

        response = self.client.get(f'/mailing/{self.mailing_id}')
        self.assertEqual(response.status_code, 200)

    def test_login_to_account_and_go_to_blog_list(self):
        self.client.login(email='test@mail.ru', password='123qwe456rty')
        response = self.client.get('/mailings/')
        self.assertEqual(response.status_code, 200)

        mailing_count = Mailing.objects.count()
        self.assertEqual(mailing_count, 1)

    def test_one_mailing(self):
        mailing = Mailing.objects.get(pk=self.mailing_id)
        mailing.client_email = mailing.client.first().email

        self.assertEqual(mailing.periodicity, 'Раз в неделю')
        self.assertEqual(mailing.client_email, 'client@mail.ru')
        self.assertEqual(mailing.message.title, 'Test')
        self.assertEqual(mailing.owner.email, 'test@mail.ru')

    def test_update_mailing(self):
        mailing = Mailing.objects.get(pk=self.mailing_id)
        mailing.client_email = mailing.client.first().email

        mailing.periodicity = 'Раз в день'
        mailing.ended_at -= datetime.timedelta(weeks=1) + datetime.timedelta(days=1)
        mailing.status = 'Создана'
        mailing.message.title = 'Hello, World!'
        mailing.client_email = 'oleg.maslov@mail.ru'

        mailing.save()

        self.assertEqual(mailing.periodicity, 'Раз в день')
        self.assertEqual(mailing.status, 'Создана')
        self.assertEqual(mailing.message.title, 'Hello, World!')
        self.assertEqual(mailing.client_email, 'oleg.maslov@mail.ru')
