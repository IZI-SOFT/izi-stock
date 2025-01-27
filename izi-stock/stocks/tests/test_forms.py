from django.test import TestCase
from stocks.models import *
from stocks.forms import *


class BranchFormTest(TestCase):
    """Test form"""

    def test_form_valid(self):
        data = {
            'description': 'Main Branch',
            'location': 'City Center'
        }
        form = BranchForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):

        data = {
            'description':'',
            'location':'City Center'
        }
        form = BranchForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_widgets(self):
        form = BranchForm()
        self.assertIn('class="form-control"', form.as_p())



class StockFormTest(TestCase):
    """Test if stock is valid with proper data"""
    def setUp(self):
        self.branch = Branch.objects.create(
            description='Main Branch',
            location='City Center'
        )

    def test_form_valid(self):
        data = {
            'description': 'Main Branch',
            'branch': self.branch
        }

        form = StockForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        data = {
            'description': '',
            'branch': self.branch
        }

        form = StockForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)


    def test_branch_queryset(self):
        """Test if the branch queryset is properly set"""
        form = StockForm()
        self.assertEqual(list(form.fields['branch'].queryset), [self.branch])


    def test_widgets(self):
        form = StockForm()
        self.assertIn('class="form-control"', form.as_p())






