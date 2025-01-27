from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from stocks.models import Branch
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import User, Stock
from django.contrib.auth import authenticate


class CustomLoginForm(AuthenticationForm):
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.filter(is_active=1),
        # empty_label="Sélectionnez une succursale",
        required=True,
        label="Succursale",
        widget=forms.Select(attrs={
            'class': 'form-control ',
            'placeholder': 'Choisissez une succursale'

        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        label="Se souvenir de moi",
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )



    # def clean(self):
    #     cleaned_data = super().clean() # appelle la validation  du parent (inclut la validation de l'utilisateur)
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')
    #
    #
    #     user = authenticate(username=username, password=password)
    #
    #
    #         #  valider que l'utilisateur est actif ou autre condition
    #     if not user.is_active:
    #         raise forms.ValidationError("Ce compte est désactivé.")
    #
    #     if not user:
    #         raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect")
    #
    #     return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'assigned_stocks', 'assigned_branches')

    assigned_stocks = forms.ModelMultipleChoiceField(
        queryset=Stock.objects.all(),
        widget=FilteredSelectMultiple("Stocks", is_stacked=False),
        required=False,
    )
    assigned_branches = forms.ModelMultipleChoiceField(
        queryset=Branch.objects.all(),
        widget=FilteredSelectMultiple("Branches", is_stacked=False),
        required=False,
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'assigned_stocks', 'assigned_branches')

    assigned_stocks = forms.ModelMultipleChoiceField(
        queryset=Stock.objects.all(),
        widget=FilteredSelectMultiple("Stocks", is_stacked=False),
        required=False,
    )
    assigned_branches = forms.ModelMultipleChoiceField(
        queryset=Branch.objects.all(),
        widget=FilteredSelectMultiple("Branches", is_stacked=False),
        required=False,
    )
