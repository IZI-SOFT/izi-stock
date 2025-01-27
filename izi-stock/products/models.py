from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
import re
from django.db.models import ProtectedError
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import request


def validate_phone_number(value):
    pattern = r'^\+?\d{1,3}?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}$'
    if not re.match(pattern, value):
        raise ValidationError(f'{value} n\'est pas un numéro de téléphone valide.')


# Modèle fournisseur

class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('kg','Kilogramme'),
        ('mg','Milligramme'),
        ('l','Litre'),
        ('ml','Millilitre'),
        ('unit', 'Unité')
    ]
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField(default=0, blank=False, null=False)
    unit = models.CharField(max_length=120, choices=UNIT_CHOICES)
    quantity = models.PositiveIntegerField(default=0, blank=False, null=False)  # Quantité en stock
    manufacture_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


    def is_expired(self):
        """Vérifie si le produit est périmé"""
        if self.expiration_date:
            return self.expiration_date < timezone.now().date()
        return False
