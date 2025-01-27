from django.utils import timezone

from django.test import TestCase
from products.models import *

class SupplierModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Supplier1",
            adresse='Supplier1_adresse',
            phone_number='22490088602'
        )

    def test_supplier_create(self):
        """ voir si le fournisseur est crée avec succes"""
        supplier = self.supplier
        self.assertEqual(supplier.name, "Supplier1")
        self.assertEqual(supplier.adresse, "Supplier1_adresse")
        self.assertEqual(supplier.phone_number, "22490088602")
        self.assertIsNotNone(supplier.created_at)

    def test_supplier_create_with_invali_phone_number(self):
        with self.assertRaises(Exception):
            supplier = Supplier.objects.create(
                name="Supplier1",
                adresse='Supplier1_adresse',
                phone_number='22490088602ABC'
            )

    def test_supplier_name_is_unique(self):
        with self.assertRaises(Exception):
            supplier = Supplier.objects.create(
                name="Supplier1",
                adresse='Supplier1_adresse',
                phone_number='22490088602'
            )

    def test_supplier_name_is_blank(self):
        with self.assertRaises(Exception):
            supplier = Supplier.objects.create(
                name=None,
                adresse='Supplier1_adresse',
                phone_number='22490088602'
            )


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Category1",
            description="Category1_description"
        )

    def test_category_create(self):
        category = self.category
        self.assertEqual(category.name,"Category1")
        self.assertEqual(category.description,"Category1_description" )
        self.assertIsNotNone(category.created_at)


    def test_category_name_is_unique(self):
        with self.assertRaises(Exception):
            category =category.objects.create(
                name="Category1",
                description="Category1_description"
            )

    def test_category_name_is_blank_or_null(self):
        with self.assertRaises(Exception):
            category = self.category.create(
                name=None,
                description="Category1_description"
            )


class ProductModelTest(TestCase):
    def setUp(self):
        self.category=Category.objects.create(
            name="Category1",
            description="Category1_description"
        )
        self.product = Product.objects.create(
            name="Product1",
            description="Product1_description",
            price="10000",
            quantity=5,
            category=self.category,
            manufacture_date='20250119',
            expiration_date='20300119'

        )

    def test_product_create(self):
        product = self.product
        self.assertEqual(product.name,"Product1")
        self.assertEqual(product.description, "Product1_description")
        self.assertEqual(product.price, "10000")
        self.assertEqual(product.quantity, 5)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.manufacture_date, '20250119')
        self.assertEqual(product.expiration_date, '20300119')

    def test_product_is_unique(self):
        with self.assertRaises(Exception):
            product=Product.objects.create(
                name="Product1",
                description="Product1_description",
                price="10000",
                quantity=5,
                category=self.category,
                manufacture_date='20250119',
                expiration_date='20300119'
            )

    def test_product_is_blank_or_null(self):
        with self.assertRaises(Exception):
            product = Product.objects.create(
                name=None,
                description="Product1_description",
                price="10000",
                quantity=5,
                category=self.category,
                manufacture_date='20250119',
                expiration_date='20300119'
            )