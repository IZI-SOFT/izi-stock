from django import forms
from .models import *
from users.models import User


class BranchForm(forms.ModelForm):
    is_active = forms.BooleanField(
        label="Statut Actif:",  # Personnalisation du label
        required=False  # Optionnel : rendre ce champ non obligatoire si nécessaire
    )

    class Meta:
        model = Branch
        fields = ['description', 'location', 'is_active']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control ',

            }),

        }


class StockForm(forms.ModelForm):
    is_active = forms.BooleanField(
        label="Statut Actif:",  # Personnalisation du label
        required=False  # Optionnel : rendre ce champ non obligatoire si nécessaire
    )

    class Meta:
        model = Stock
        fields = ['description', 'branch', 'is_active']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',

                'is_active': forms.CheckboxInput(attrs={
                    'class': 'form-control'
                })
            }),
            'branch': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Définir les choix pour le champ Branch
        self.fields['branch'].queryset = Branch.objects.all()


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['number', 'date_of_purchase', 'stock']
        widgets = {
            'stock': forms.Select(attrs={
                'class': 'form-control price-field'
            }),
            'number': forms.TextInput(attrs={
                'class': 'form-control',

            }),
            'date_of_purchase': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        branch = kwargs.pop('branch', None)
        super().__init__(*args, **kwargs)
        if user and branch:
            self.fields['stock'].queryset = Stock.objects.filter(user=user, branch=branch)
        elif user:
            self.fields['stock'].queryset = Stock.objects.filter(user=user)
        else:
            self.fields['stock'].queryset = Stock.objects.none()


class InvoiceLineForm(forms.ModelForm):
    class Meta:
        model = InvoiceLine
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
