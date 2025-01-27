from django.test import TestCase
from products.models import *
from products.forms import *


class CategoryFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'name': 'category1',
            'description': 'category_description'
        }
        form = CategoryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'name': '',
            'description': 'category_description'
        }
        form = CategoryForm(data=data)
        self.assertFalse(form.is_valid())


class ProductFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='category',
            description='category_description'
        )

    def test_valid_form(self):
        data = {
            'name': 'product1',
            'description': 'product1_description',
            'category': self.category.id,
            'price': 1000,
            'quantity': 30,
            'manufacture_date': '2025-01-01',
            'expiration_date': '2026-01-01'
        }

        form = ProductForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_form_name_is_blank_or_None(self):
        data = {
            'name': None,
            'description': 'product1_description',
            'category': self.category.id,
            'price': 1000,
            'quantity': 30,
            'manufacture_date': '2025-01-01',
            'expiration_date': '2026-01-01'
        }

        form = ProductForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_invalid_manufacture_expiration_date(self):
        data = {
            'name': "product1",
            'description': 'product1_description',
            'category': self.category.id,
            'price': 1000,
            'quantity': 30,
            'manufacture_date': '2025-01-01',
            'expiration_date': '2024-01-01'
        }

        form = ProductForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)


class SupplierFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'name': 'supplier1',
            'adresse': 'lome',
            'phone_number': '90088602'
        }
        form = SupplierForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_form_name_blank_or_null(self):
        data = {
            'name': None,
            'adresse': 'lome',
            'phone_number': '90088602'
        }
        form = SupplierForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_invalid_form_phone_invalid(self):
        data = {
            'name': 'supplier1',
            'adresse': 'lome',
            'phone_number': '90088602abv'
        }
        form = SupplierForm(data=data)
        self.assertFalse(form.is_valid(), form.errors)
