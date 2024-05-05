from django.contrib.auth.hashers import make_password
from django.test import TestCase

from mailsender_app.models import Client
from mailsender_app.services import create_user


class ClientTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = 1

    @classmethod
    def setUpTestData(cls):
        user = create_user()

        Client.objects.create(name='Client', surname='Clientov', email='client@mail.ru', owner=user)

    def login_and_go_to_client_page(self):
        self.client.login(email='test@mail.ru', password='123qwe456rty')

        response = self.client.get(f'/client/{self.client_id}')
        self.assertEqual(response.status_code, 301)

        return response

    def test_login_to_account_and_go_to_client_list(self):
        self.client.login(email='test@mail.ru', password='123qwe456rty')
        response = self.client.get('/clients/')
        self.assertEqual(response.status_code, 200)

        client_count = Client.objects.count()
        self.assertEqual(client_count, 1)

    def test_one_client(self):
        response = self.login_and_go_to_client_page()

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

        client = Client.objects.get(pk=self.client_id)

        self.assertEqual(client.name, 'Client')
        self.assertEqual(client.surname, 'Clientov')
        self.assertEqual(client.email, 'client@mail.ru')

    def test_update_client(self):
        client = Client.objects.get(pk=self.client_id)

        client.name = 'Oleg'
        client.surname = 'Maslov'
        client.email = 'oleg.maslov@mail.ru'

        client.save()

        self.assertEqual(client.name, 'Oleg')
        self.assertEqual(client.surname, 'Maslov')
        self.assertEqual(client.email, 'oleg.maslov@mail.ru')
