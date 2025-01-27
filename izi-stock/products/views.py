from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    ordering = ['-created_at']

    # fonction de recherche sur la liste
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Récupérer la valeur du champ de recherche
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_add.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'products/category_add.html'
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    template_name = 'category_confirm_delete.html'

    def post(self, request, *args, **kwargs):

        try:
            messages.success(request, "La catégorie a été supprimée avec succès")
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request,
                           "Impossible de supprimer cette catégorie car elle est référencée par des produits.")
            """Redirige vers la liste des catégories après une erreur."""
            return HttpResponseRedirect(self.success_url)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    paginate_by = 10

    # fonction de recherche sur la liste
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Récupérer la valeur du champ de recherche
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_add.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # appel de la méthode parente pour enregistre l'objet
        response = super().form_valid(form)
        # Ajout d'un message de succès
        messages.success(self.request, "Le produit a été créé avec succès.")

        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/product_add.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')

    def post(self, request, *args, **kwargs):

        try:
            messages.success(request, "Le produit a été supprimée avec succès")
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request,
                           "Impossible de supprimer ce produit car il est référencé par des entrées en stock.")
            """Redirige vers la liste des catégories après une erreur."""
            return HttpResponseRedirect(self.success_url)


class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'products/supplier_list.html'
    context_object_name = 'supplies'
    ordering = ['-created_at']
    paginate_by = 10

    # fonction de recherche sur la liste
    def get_queryset(self):
        queryset = super().get_queryset()  # récuper le queryset parent qui correspond à tous les objets de la database
        query = self.request.GET.get('q')  # récupère la valeur du paramètre 'q' dans la requete GET
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'products/supplier_add.html'
    success_url = reverse_lazy("supplier_list")

    def form_valid(self, form):
        # appel de la méthode parente pour enregistre l'objet
        response = super().form_valid(form)
        # Ajout d'un message de succès
        messages.success(self.request, "Le fournisseur a été créé avec succès.")
        return response


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'products/supplier_add.html'
    success_url = reverse_lazy('supplier_list')


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    success_url = reverse_lazy('supplier_list')

    def post(self, request, *args, **kwargs):

        try:
            messages.success(request, "Le fournisseur a été supprimée avec succès")
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request,
                           "Impossible de supprimer ce fournisseur car il est référencé par des entrées en stock.")
            """Redirige vers la liste des catégories après une erreur."""
            return HttpResponseRedirect(self.success_url)
