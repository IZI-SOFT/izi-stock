from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('branches/add/',branch_add, name='branches_add' ),
    path('branches/list/',branch_list, name='branches_list' ),
    path('branches/edit/<int:pk>',branch_edit, name='branches_edit' ),
    path('branches/delete/<int:pk>',branch_delete, name='branches_delete' ),
    path('stock/add/', stock_add, name='stock_add'),
    path('stock/list/', stock_list, name='stock_list'),
    path('stock/edit/<int:pk>', stock_edit, name='stock_edit'),
    path('stock/delete/<int:pk>', stock_delete, name='stock_delete'),
    path('invoice/add/',InvoiceCreateView.as_view(), name='invoice_add' ),
    path('invoice/list/',InvoiceListView.as_view(), name='invoice_list' ),
    path('invoice/<int:invoice_pk>/line/', InvoiceLineCreateView.as_view(), name='invoice_line_add'),
]