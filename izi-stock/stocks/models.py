from django.db import models
from django.utils.timezone import now
from products.models import *
from users.models import *
from django.utils import timezone


class Branch(models.Model):
    description = models.CharField(max_length=255, unique=True, blank=False, null=False)
    location = models.CharField(max_length=255, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class Stock(models.Model):
    description = models.CharField(max_length=255, unique=True, blank=False, null=False)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='stocks')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description


class Invoice(models.Model):
    number = models.CharField(max_length=255, unique=True)
    date_of_purchase = models.DateField(default=timezone.now)
    total_amount = models.PositiveIntegerField(default=0)
    branch = models.ForeignKey('stocks.Branch', on_delete=models.PROTECT)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    supplier = models.ForeignKey('products.Supplier', on_delete=models.PROTECT )
    created_by = models.ForeignKey('users.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.number} - {self.date_of_purchase}"

    def update_total(self):
        """Met à jour le total de la facture en fonction des lignes de produit"""
        total = sum(line.total for line in self.lines.all())
        self.total_amount = total
        self.save()


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='lines', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    total = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):
        """Calcule le total de chaque ligne avant de sauvegarder"""
        self.total = self.quantity*self.unit_price
        super().save(*args, **kwargs)
