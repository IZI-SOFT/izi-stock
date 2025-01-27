from django.test import TestCase
from users.models import User
from django.urls import reverse
from ..forms import *
from ..models import *


class CategoryListViewTest(TestCase):
    def setUp(self):
        """création d'un utilisateur"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.url = reverse('category_list')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_if_logged_in(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category_list.html')


class CategoryCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.category_data = {
            'name': 'category1',
            'description': 'category1_description'
        }

        self.url = reverse('category_add')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_if_logged_in(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category_add.html')
        self.assertIsInstance(response.context["form"], CategoryForm)

    def test_category_post_valid_form(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, self.category_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('category_list'))
        self.assertEqual(Category.objects.count(), 1)
        category = Category.objects.first()
        self.assertEqual(category.name, 'category1')
        self.assertEqual(category.description, 'category1_description')

    def test_category_post_invalid_form(self):
        self.client.login(username="testuser", password="testpassword")
        invalid_data = {
            'name': '',
            'description': 'category1_description'
        }
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category_add.html')
        self.assertFalse(Category.objects.filter(name='').exists())


class CategoryEditViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(name="category1", description="category_description")

        self.url = reverse('category_edit', args=[self.category.pk])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_if_logged_in(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category_add.html')
        self.assertIsInstance(response.context["form"], CategoryForm)
        self.assertEqual(response.context['form'].instance, self.category)

    def test_category_post_valid_form(self):
        self.client.login(username="testuser", password="testpassword")
        valid_data = {"name": "category1Update", "description": "category_update_description"}
        response = self.client.post(self.url, valid_data)
        self.assertRedirects(response, reverse("category_list"))
        self.category.refresh_from_db()  # Recharge l'objet de la base de données
        self.assertEqual(self.category.name, "category1Update")
        self.assertEqual(self.category.description, "category_update_description")

    def test_category_post_invalid_form(self):
        self.client.login(username="testuser", password="testpassword")
        invalid_data = {"name": "", "description": ""}
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Category.objects.filter(name="").exists())


class CategoryDeleteTest(TestCase):
    def setUp(self):
        """configurer les données initiales pour les tests"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Créer un objet Category pour tester la suppression
        self.category = Category.objects.create(name="category1", description="category1_description")

        # URL pour la suppression de la branche
        self.url = reverse('category_delete', args=[self.category.pk])

    def test_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_delete_category_post(self):
        """Tester la suppression d'une catégorie avec une requête POST"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url)

        # Vérifier si la catégorie est supprimée
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())

        # Vérifier la redirection vers la liste des branches
        self.assertRedirects(response, reverse("category_list"))


class ProductListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.url = reverse('product_list')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_access_if_logged_in(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')


class ProductCreateViewTest(TestCase):
    def setUp(self):
        """Configuration initiale des tests"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name="category1",
            description="category1_description"
        )
        self.product_data = {
            "name": "Product1",
            "description": "Product1_description",
            "price": 1000,
            "quantity": 20,
            "category": self.category.id,
            "manufacture_date": "2025-01-01",
            "expiration_date": "2026-01-01"
        }
        self.url = reverse('product_add')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_access_if_logged_in(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_add.html')
        self.assertIsInstance(response.context["form"], ProductForm)

    def test_post_valid_form(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, self.product_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("product_list"))
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.name, "Product1")
        self.assertEqual(product.description, "Product1_description")

    def test_post_invalid_form(self):
        """Tester si un formulaire invalide retourne la même page avec des erreurs"""
        self.client.login(username="testuser", password="testpassword")
        invalid_data = {"name": "", "description": ""}  # Données invalides
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_add.html")
        self.assertFalse(Product.objects.filter(description='').exists())


class ProductUpdateViewTest(TestCase):
    def setUp(self):
        """initialisation des données pour les tests"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        self.category = Category.objects.create(
            name="category1",
            description="category1_description"
        )
        self.product = Product.objects.create(
            name="Product1",
            description="product1_description",
            price=1000,
            quantity=5,
            category=self.category,
            manufacture_date='2025-01-01',
            expiration_date='2026-01-01'
        )

        self.url = reverse('product_edit', args=[self.product.pk])  # URL pour la vue branch_edit

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_get_valid_branch_edit_page(self):
        """Tester si la page de modification du produit est accessible pour un utilisateur connecté."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_add.html")
        self.assertIsInstance(response.context['form'], ProductForm)
        self.assertEqual(response.context['form'].instance, self.product)

    def test_post_valid_form(self):
        self.client.login(username="testuser", password="testpassword")
        valid_data = {
            "name": "Product1_update",
            "description": "Product1_description_description",
            "price": 1000,
            "quantity": 20,
            "category": self.category.id,
            "manufacture_date": "2025-01-01",
            "expiration_date": "2026-01-01"
        }
        response = self.client.post(self.url, valid_data)
        self.assertRedirects(response, reverse('product_list'))  # Vérifie la redirection
        self.product.refresh_from_db()  # Recharge l'objet de la base de données
        self.assertEqual(self.product.name, "Product1_update")
        self.assertEqual(self.product.description, "Product1_description_description")


    def test_post_invalid_form(self):
        self.client.login(username="testuser", password="testpassword")
        invalid_data = {
            "name": "",
            "description": "",
            "price": 1000,
            "quantity": 20,
            "category": self.category.id,
            "manufacture_date": "2025-01-01",
            "expiration_date": "2026-01-01"
        }
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code,200)
        self.assertFalse(Product.objects.filter(name="").exists())


class ProductDeleteViewTest(TestCase):
    def setUp(self):
        """initialisation des données pour les tests"""
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        self.category = Category.objects.create(
            name="category1",
            description="category1_description"
        )
        self.product = Product.objects.create(
            name="Product1",
            description="product1_description",
            price=1000,
            quantity=5,
            category=self.category,
            manufacture_date='2025-01-01',
            expiration_date='2026-01-01'
        )

        self.url = reverse('product_delete', args=[self.product.pk])  # URL pour la vue branch_edit

    def test_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_delete_produt_post(self):
        """Tester la suppression d'une branche avec une requête POST"""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url)

        # Vérifier si le produit est supprimée
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

        # Vérifier la redirection vers la liste des branches
        self.assertRedirects(response, reverse("product_list"))