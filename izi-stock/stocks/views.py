from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import redirect, get_object_or_404
from .forms import *
from .models import *
from django.contrib import messages
from django.db.models.deletion import ProtectedError


# vue du dashboard
@login_required()
def dashboard(request):
    return render(request, 'dashboard.html', {})


# les vues liées à Branch
@login_required()
def branch_list(request):
    query = request.GET.get('q')  # récupère la valeur du champ de recherche
    if query:
        branches = Branch.objects.filter(description__icontains=query).order_by('-created_at')
    else:
        branches = Branch.objects.all().order_by('-created_at')
        # créer un paginator
        paginator = Paginator(branches, per_page=10)
        # récuperer le numéro de la page actuelle
        page_number = request.GET.get('page')

        page_obj = paginator.get_page(page_number)

    return render(request, 'stocks/branch_list.html', {'branches': branches, 'page_obj': page_obj})


@login_required()
def branch_add(request):
    if request.method == "POST":
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "La succursale a été créée avec succès")
            return redirect("branches_list")
    else:
        form = BranchForm()

    return render(request, "stocks/branch_add.html", {'form': form})


@login_required()
def branch_edit(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == "POST":
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, "Les modifications ont été effectuées  avec succès")
            return redirect("branches_list")
    else:
        form = BranchForm(instance=branch)

    return render(request, "stocks/branch_add.html", {'form': form})


@login_required()
def branch_delete(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    try:
        branch.delete()
        messages.success(request, "La Succursale est supprimée avec succès ")
    except ProtectedError:
        messages.error(request, "Impossible de supprimer cette succursale car elle est référencée par des stocks")
    return redirect("branches_list")


# les vues liées au Stock

@login_required()
def stock_list(request):
    # récupérer ce que l'user a saisi dans le formulaire du  template stock_list_.html
    query = request.GET.get('q')
    # récupére les succursales de l'ulisateur
    assigned_branches = request.user.assigned_branches.all()
    if query:
        stocks = Stock.objects.filter(description__icontains=query,
                                      branch__in=assigned_branches)  # filtre sur la recherche

    else:
        stocks = Stock.objects.filter(branch__in=assigned_branches).order_by('-created_at')
        per_page = 10  # nombre d'éléments par page
        #créer un paginator
        paginator = Paginator(stocks, per_page)
        # récuper le numéro de la page actuelle
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, "stocks/stock_list.html", context={'stocks': stocks, 'page_obj': page_obj})


@login_required()
def stock_add(request):
    if request.method == 'POST':
        # Passe les données POST au formulaire
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde si valide
            messages.success(request, "Le stock a été créé avec succès")
            return redirect('stock_list')
    else:
        # Initialise le formulaire sans données
        form = StockForm()

    return render(request, 'stocks/stock_add.html', {'form': form})


@login_required()
def stock_edit(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == "POST":
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, "Le stock a été modifié avec succès")
            return redirect('stock_list')
    else:
        form = StockForm(instance=stock)

    return render(request, "stocks/stock_add.html", {'form': form})


@login_required()
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    try:
        stock.delete()
        messages.success(request, "Le stock est supprimé avec succès")
    except ProtectedError:
        messages.error(request, "Impossible de supprimer cette succursale")
    return redirect("stock_list")


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'stocks/invoice_list.html'
    context_object_name = 'invoices'
    ordering = ['-created_at']
    paginate_by = 10

    # fonction de recherche sur la liste
    def get_queryset(self):
        queryset = super().get_queryset()  # récuper le queryset parent qui correspond à tous les objets de la database
        query = self.request.GET.get('q')  # récupère la valeur du paramètre 'q' dans la requete GET
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'stocks/invoice_add.html'
    success_url = reverse_lazy('invoice_list')

    def form_valid(self, form):
        # Récupère la succursale active dans la session
        branch_id = self.request.session.get('selected_branch')
        if not branch_id:
            form.add_error(None, "Aucune succursale sélectionnée")
            return self.form_invalid(form)

        # Associe les champs branch et created_by avant l'enregistrement
        form.instance.branch_id = branch_id
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        """ajoute l'utilisateur connecté auw kwargs du formulaire"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        # Récupération de la succursale depuis le context processor
        branch = self.request.session.get('branch_id')  # Récupère l'ID de la succursale
        kwargs['branch'] = Branch.objects.filter(id=branch).first() if branch else None
        return kwargs


class InvoiceLineCreateView(FormView):
    template_name = 'stocks/invoice_line_add.html'
    form_class = InvoiceLineForm

    def get_invoice(self):
        return get_object_or_404(Invoice, pk=self.kwargs['invoice_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.get_invoice()
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        invoice = self.get_invoice()
        line = form.save(commit=False)
        line.invoice = invoice
        # met à jour le total de la facture
        invoice.update_total()
        # Redirige vers la page de création des lignes de facture
        return redirect('invoice_line_add', pk=invoice.pk)
