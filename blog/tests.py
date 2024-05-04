from django.contrib.auth.hashers import make_password
from django.test import TestCase

from blog.models import Blog
from users.models import User


class BlogTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blog_id = 2

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            first_name='Test',
            last_name='Testov',
            email='test@mail.ru',
            password=make_password('123qwe456rty')
        )
        number_of_blogs = 5
        for blog_id in range(number_of_blogs):
            Blog.objects.create(title=f'Title for blog {blog_id}', body=f'Body for blog {blog_id}')

    def login_and_go_to_one_blog_material(self):
        self.client.login(email='test@mail.ru', password='123qwe456rty')

        response = self.client.get(f'/blog/{self.blog_id}')
        self.assertEqual(response.status_code, 301)

        return response

    def test_login_to_account_and_go_to_blog_list(self):
        self.client.login(email='test@mail.ru', password='123qwe456rty')
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        blog_count = Blog.objects.count()
        self.assertEqual(blog_count, 5)

    def test_one_blog_material(self):
        response = self.login_and_go_to_one_blog_material()

        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)

        blog = Blog.objects.get(pk=self.blog_id)

        self.assertEqual(blog.title, f'Title for blog {self.blog_id - 1}')
        self.assertEqual(blog.body, f'Body for blog {self.blog_id - 1}')

    def test_blog_update(self):
        blog = Blog.objects.get(pk=self.blog_id)
        blog.title = 'New title for blog'
        blog.save()

        self.assertEqual(blog.title, 'New title for blog')
