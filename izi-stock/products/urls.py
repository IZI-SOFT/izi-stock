from django.urls import path, include
from .views import *

urlpatterns = [

    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_add'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='category_edit'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('supplies/', SupplierListView.as_view(), name='supplier_list'),
    path('supplier/add/', SupplierCreateView.as_view(), name='supplier_add'),
    path('supplier/edit/<int:pk>/', SupplierUpdateView.as_view(), name='supplier_edit'),
    path('supplier/delete/<int:pk>/', SupplierDeleteView.as_view(), name='supplier_delete'),

]