from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command


class TestMainappSmoke(TestCase):

    status_code_success = 200

    def setUp(self):
        # call_command('flush', '--noinput')
        # imitation of the "python manage.py loaddata test_db.json":
        # call_command('loaddata', 'test_db.json')
        self.client = Client()
        # alternative way to prepare the database manual:
        cat_1 = ProductCategory.objects.create(
            name='cat_1'
        )
        Product.objects.create(
            category=cat_1,
            name='prod_1'
        )

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

        # There is no "contact" page in my project:
        # response = self.client.get('/contact/')
        # self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.status_code_success)

        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, self.status_code_success)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)
        # No single pages for the products in my templates:
        # for product in Product.objects.all():
        #     response = self.client.get(f'/products/product/{product.pk}/')
        #     self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
