from django.test import TestCase
from stocks.models import *


class BranchModelTest(TestCase):

    def setUp(self):
        """Initial setup for the tests."""
        self.branch = Branch.objects.create(
            description="Main Branch",
            location="City Center"
        )

    def test_branch_creation(self):
        """Test if a branch instance is created successfully."""
        branch = self.branch
        self.assertEqual(branch.description, "Main Branch")
        self.assertEqual(branch.location, "City Center")
        self.assertIsNotNone(branch.created_at)

    def test_description_is_unique(self):
        """Test if a branch description is unique"""
        with self.assertRaises(Exception):
            branch = Branch.objects.create(
                description="Main Branch",
                location="City Center 2"
            )

    def test_fields_cannot_be_blank_or_null(self):
        with self.assertRaises(Exception):
            Branch.objects.create(description=None, location="valid location")

        with self.assertRaises(Exception):
            Branch.objects.create(description="valid description", location=None)


    def test_delete_branch_protect(self):
        # vérifier que la brache existe avant la suppression
        self.assertEqual(Branch.objects.count(),1)
        with self.assertRaises(Exception):
            self.branch.delete()
            self.assertEqual(Branch.objects.count(), 1)

    def test_str_method(self):
        """Test the string representation of the model"""
        branch = Branch.objects.get(description="Main Branch")
        self.assertEqual(str(branch), "Main Branch")


class StockModelTest(TestCase):
    """Test if stock instance is created"""

    def setUp(self):
        self.branch = Branch.objects.create(
            description="Main Branch",
            location="Lomé"
        )
        self.stock = Stock.objects.create(
            description="LA TERRAZZA",
            branch=self.branch
        )

    def test_stock_creation(self):
        stock = self.stock
        self.assertEqual(stock.description, "LA TERRAZZA")
        self.assertEqual(stock.branch, self.branch)
        self.assertIsNotNone(stock.created_at)

    def test_stock_description_is_unique(self):
        with self.assertRaises(Exception):
            self.stock.objects.create(
                description="LA TERRAZZA",
                branch=self.branch
            )

    def test_fields_is_blank_or_null(self):
        with self.assertRaises(Exception):
            self.stock.objects.create(description=None, branch=self.branch)

        with self.assertRaises(Exception):
            self.stock.objects.create(description="Valid description", branch=None)

    def test_delete_stock(self):
        # vérifier que le stock existe avant la suppression
        self.assertEqual(Stock.objects.count(),1)
        # Supprimer le stock
        self.stock.delete()
        self.assertEqual(Stock.objects.count(),0)

