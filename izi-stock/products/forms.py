from .models import *
from django import forms


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'unit', 'price', 'quantity', 'manufacture_date', 'expiration_date']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control price-field'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'unit':forms.Select(attrs={
                'class': 'form-control'
            }),

            'manufacture_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'expiration_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

        }

    def clean(self):
        """cette méthode si la date de péremption est postérieure à la date de fabrication"""
        cleaned_data = super().clean()
        manufacture_date = cleaned_data.get("manufacture_date")
        expiration_date = cleaned_data.get("expiration_date")

        if expiration_date and manufacture_date:
            if expiration_date <= manufacture_date:
                raise forms.ValidationError(
                    "La date de péremption doit être postérieure à la date de fabrication."
                )



class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'adresse', 'phone_number']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'adresse': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }
