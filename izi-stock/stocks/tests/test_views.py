from django.test import TestCase
from ..views import *
from django.urls import reverse
from users.models import User
from ..models import *
from ..forms import *


class DashboardViewTest(TestCase):
    def setUp(self):
        """Créer un utilisateur pour les tests"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.url = reverse('dashboard')

    def test_redirect_if_not_logged_in(self):
        """rediriger vers la page d'acceuil si utilisateur non connecté"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_access_if_logged_in(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')


class BranchListViewTest(TestCase):
    """Tester la vue de la liste des succursales"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.url = reverse('branches_list')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_access_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocks/branch_list.html')


class BranchAddViewTest(TestCase):
    def setUp(self):
        """Configuration initiale des tests"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.branch_data = {
            "description": "Main Branch",
            "location": "City Center"
        }
        self.url = reverse('branches_add')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_access_if_logged_in(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocks/branch_add.html')
        self.assertIsInstance(response.context["form"], BranchForm)

    def test_post_valid_form(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, self.branch_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("branches_list"))
        self.assertEqual(Branch.objects.count(), 1)
        branch = Branch.objects.first()
        self.assertEqual(branch.description, "Main Branch")
        self.assertEqual(branch.location, "City Center")

    def test_post_invalid_form(self):
        """Tester si un formulaire invalide retourne la même page avec des erreurs"""
        self.client.login(username="testuser", password="testpassword")
        invalid_data = {"description": "", "location": ""}  # Données invalides
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stocks/branch_add.html")
        self.assertFalse(Branch.objects.filter(description='').exists())


class BranchEditViewTest(TestCase):
    """ test la modification d'une branche créé"""

    def setUp(self):
        """initialisation des données pour les tests"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.branch = Branch.objects.create(description="Main Branch", location="City Center")
        self.url = reverse('branches_edit', args=[self.branch.pk])  # URL pour la vue branch_edit

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_get_valid_branch_edit_page(self):
        """Tester si la page de modification de la branche est accessible pour un utilisateur connecté."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stocks/branch_add.html")
        self.assertIsInstance(response.context['form'], BranchForm)
        self.assertEqual(response.context['form'].instance, self.branch)

    def test_post_valid_form(self):
        """Tester si un formulaire valide met à jour la branche et redirige"""
        self.client.login(username="testuser", password="testpassword")
        valid_data = {"description": "Updated Branch", "location": "Updated location"}
        response = self.client.post(self.url, valid_data)
        self.assertRedirects(response, reverse('branches_list'))  # Vérifie la redirection
        self.branch.refresh_from_db()  # Recharge l'objet de la base de données
        self.assertEqual(self.branch.description, "Updated Branch")
        self.assertEqual(self.branch.location, "Updated location")

    def test_post_invalid_form(self):
        """Tester si un formulaire invalide retourne la même page avec des erreurs."""
        self.client.login(username="testuser", password="testpassword")
        invalid_data = {'description': "", 'location': ""}
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Branch.objects.filter(description="").exists())


class BranchDeleteViewTest(TestCase):
    def setUp(self):
        """configurer les données initiales pour les tests"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Créer un objet Branch pour tester la suppression
        self.branch = Branch.objects.create(description="Main Branch", location="City Center")

        # URL pour la suppression de la branche
        self.url = reverse('branches_delete', args=[self.branch.pk])

    def test_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_delete_branch_post(self):
        """Tester la suppression d'une branche avec une requête POST"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url)

        # Vérifier si la branche est supprimée
        self.assertFalse(Branch.objects.filter(pk=self.branch.pk).exists())

        # Vérifier la redirection vers la liste des branches
        self.assertRedirects(response, reverse("branches_list"))


class StockListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.url = reverse('stock_list')

    def test_if_is_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_stock_list_get(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocks/stock_list.html')


class StockAddViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.url = reverse('stock_add')
        self.branch = Branch.objects.create(description="Main Branch", location="City Center")
        self.valid_data = {'description': "valid_stock", 'branch': self.branch.pk}

    def test_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_post_valid_form(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, self.valid_data)
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('stock_list'))
        self.assertEqual(Stock.objects.count(), 1)
        stock = Stock.objects.first()
        self.assertEqual(stock.description, "valid_stock")

    def test_post_invalid_form(self):
        invali_data = {'description': 'valid_stock', 'branch': ''}
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, invali_data)
        self.assertEqual(response.status_code, 200)  # on reste sur la même page
        self.assertTemplateUsed(response, 'stocks/stock_add.html')
        self.assertFalse(Stock.objects.filter(branch='1').exists())


class StockEditViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.branch = Branch.objects.create(description="Main Branch", location="City Center")
        self.stock = Stock.objects.create(description="Main stock", branch=self.branch)
        self.url = reverse('stock_edit', args=[self.stock.pk])

    def test_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_get_valid_edit_page(self):
        """Tester si la page de modification du stock est accessible"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stocks/stock_add.html")
        self.assertIsInstance(response.context['form'], StockForm)
        self.assertEqual(response.context['form'].instance, self.stock)

    def test_post_valid_form(self):
        self.client.login(username="testuser", password="testpassword")
        valid_data = {'description': "Main stock", 'branch': self.branch.pk}
        response = self.client.post(self.url, data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('stock_list'))
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.description, "Main stock")

    def test_post_invalid_form(self):
        self.client.login(username="testuser", password="testpassword")
        invalid_data = {'description': '', 'branch': ''}
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stocks/stock_add.html")
        self.assertTrue(response.context['form'].errors)

        # Vérifie que l'objet n'a pas été mdodifié
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.description, "Main stock")


class StockDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.branch = Branch.objects.create(description="Main Branch", location="City Center")
        self.stock = Stock.objects.create(description="Main stock", branch=self.branch)
        self.url = reverse('stock_delete', args=[self.stock.pk])

    def test_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_delete_stock_post(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url)

        # vérifier si le stock est supprimé
        self.assertFalse(Stock.objects.filter(pk=self.stock.pk).exists())
        # vérifier la redirection vers la liste des stocks
        self.assertRedirects(response, reverse("stock_list"))
