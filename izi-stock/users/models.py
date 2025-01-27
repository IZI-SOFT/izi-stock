from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from stocks.models import Branch, Stock
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class User(AbstractUser):
    assigned_stocks = models.ManyToManyField(Stock, blank=True)
    assigned_branches = models.ManyToManyField(Branch, blank=True)

    def is_admin(self):
        return self.is_superuser  # Vérifie si l'utilisateur est admin

    def __str__(self):
        return self.username

        # vérifier si un utilisateur a accès à un stock ou une succursale spécifique

    def has_access_to_stock(self, stock):
        return self.is_superuser or stock in self.assigned_stocks.all()

    def has_access_to_branch(self, branch):
        return self.is_superuser or branch in self.assigned_branches.all()

    def validate_relations(self):
        """
        Valide que tous les stocks assignés appartiennent à une succursale assignée.
        """
        if self.assigned_stocks.exists() and self.assigned_branches.exists():
            for stock in self.assigned_stocks.all():
                if stock.branch not in self.assigned_branches.all():
                    raise ValidationError(
                        f"Le stock '{stock}' n'appartient pas à une succursale assignée."
                    )

    class Meta:
        permissions = [
            ("view_dashboard", "Peut voir le  dashboard"),
            ("view_settings", "Peut voir les paramétrages"),
            ("view_entree_stock", "Peut voir les Entrées en stock"),
            ("view_Transfert_entre_stock", "Peut voir le Transfert entre stock"),
            ("view_Inventaire", "Peut voir les inventaires"),
            ("view_reporting", "Peut voir les rapports"),
        ]


# Signal pour valider les relations Many-to-Many
def validate_m2m_relations(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove"]:
        try:
            instance.validate_relations()
        except ValidationError as e:
            # Log l'erreur pour le suivi
            logger.error(f"Validation échouée pour l'utilisateur {instance}: {e}")
            # Option : Supprimer les relations pour éviter des données incohérentes
            instance.assigned_stocks.clear()
            instance.assigned_branches.clear()
            # Option : Retourner une erreur utilisateur gracieusement
            instance._validation_error = str(e)  # Stocker le message d'erreur dans l'instance
            return  # Ne pas lever d'exception, gérer ailleurs


# Connecter le signal Many-to-Many
m2m_changed.connect(validate_m2m_relations, sender=User.assigned_stocks.through)
m2m_changed.connect(validate_m2m_relations, sender=User.assigned_branches.through)
