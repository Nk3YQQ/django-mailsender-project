from django.test import TestCase

from mailsender_app.models import Message
from mailsender_app.services import create_user


class MessageTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_id = 2

    @classmethod
    def setUpTestData(cls):
        user = create_user()

        Message.objects.create(title='Test', body='Hello, Django!', owner=user)

    def login_and_go_to_message_page(self):
        self.client.login(email='test@mail.ru', password='123qwe456rty')

        response = self.client.get(f'/message/{self.message_id}')
        self.assertEqual(response.status_code, 200)

        return response

    def test_login_to_account_and_go_to_message_list(self):
        self.client.login(email='test@mail.ru', password='123qwe456rty')
        response = self.client.get('/messages/')
        self.assertEqual(response.status_code, 200)

        message_count = Message.objects.count()
        self.assertEqual(message_count, 1)

    def test_one_message(self):
        message = Message.objects.get(pk=self.message_id)

        self.assertEqual(message.title, 'Test')
        self.assertEqual(message.body, 'Hello, Django!')

    def test_update_message(self):
        message = Message.objects.get(pk=self.message_id)

        message.title = 'New test'
        message.body = 'Hello, my project!'

        message.save()

        self.assertEqual(message.title, 'New test')
        self.assertEqual(message.body, 'Hello, my project!')
