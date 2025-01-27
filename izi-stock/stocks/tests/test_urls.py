from django.test import SimpleTestCase
from ..views import *
from django.urls import reverse, resolve


class TestUrls(SimpleTestCase):
    def test_dashboard_url_resolves(self):
        """Test si l'URL pour le tableau de bord pointe vers la vue correcte"""
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, dashboard)

    def test_branch_add_url_resolves(self):
        url = reverse('branches_add')
        self.assertEqual(resolve(url).func, branch_add)

    def test_branch_list_url_resolves(self):
        url = reverse('branches_list')
        self.assertEqual(resolve(url).func, branch_list)

    def test_branch_edit_resolves(self):
        url = reverse('branches_edit', args=[1])
        self.assertEqual(resolve(url).func, branch_edit)

    def test_branch_delete_url_resolves(self):
        """Test si l'URL pour supprimer une branche pointe vers la vue correcte"""
        url = reverse('branches_delete', args=[1])
        self.assertEqual(resolve(url).func, branch_delete)

    def test_stock_add_url_resolves(self):
        """Test si l'URL pour ajouter un stock pointe vers la vue correcte"""
        url = reverse('stock_add')
        self.assertEqual(resolve(url).func, stock_add)

    def test_stock_list_url_resolves(self):
        """Test si l'URL pour lister les stocks pointe vers la vue correcte"""
        url = reverse('stock_list')
        self.assertEqual(resolve(url).func, stock_list)

    def test_stock_edit_url_resolves(self):
        """Test si l'URL pour éditer un stock pointe vers la vue correcte"""
        url = reverse('stock_edit', args=[1])
        self.assertEqual(resolve(url).func, stock_edit)

    def test_stock_delete_url_resolves(self):
        """Test si l'URL pour supprimer un stock pointe vers la vue correcte"""
        url = reverse('stock_delete', args=[1])
        self.assertEqual(resolve(url).func, stock_delete)
