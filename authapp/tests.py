from django.test import TestCase
from django.test.client import Client
from authapp.models import User
from django.core.management import call_command

from mainapp.models import ProductCategory, Product


class TestUserManagement(TestCase):
    def setUp(self):
        # call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')
        for i in range(100):
            User.objects.create(
                username=f'user_{i}'
            )
        cat_1 = ProductCategory.objects.create(
            name='cat_1'
        )
        for i in range(100):
            Product.objects.create(
                category=cat_1,
                name=f'prod_{i}'
            )
        self.client = Client()

        self.superuser = User.objects.create_superuser('django2', 'django2@geekshop.local', 'geekbrains')
        self.user = User.objects.create_user('tarantino', 'tarantino@geekshop.local', 'geekbrains')
        self.user_with__first_name = User.objects.create_user('umaturman', 'umaturman@geekshop.local', 'geekbrains',
                                                              first_name='Ума')

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'GeekShop')
        # self.assertNotContains(response, 'Пользователь', status_code=200)
        self.assertNotIn('Мои Заказы', response.content.decode())

        # данные пользователя
        self.client.login(username='tarantino', password='geekbrains')

        # логинимся
        response = self.client.get('/users/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # главная после логина
        response = self.client.get('/')
        # print(f':::::ОТВЕТ НАШЕГО САЙТ:::::{response.content.decode()}')
        # self.assertContains(response, 'Мои Заказы', status_code=200)
        self.assertEqual(response.context['user'], self.user)
        self.assertIn('Мои Заказы', response.content.decode())

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
