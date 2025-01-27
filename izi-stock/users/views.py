from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm
from django.http import request
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from utils.models import *


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

    # affichage du logo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        izisoft = Izisoft.objects.first()
        context['logo'] = izisoft.logo.url if izisoft and izisoft.logo else None
        return context

    def form_valid(self, form):
        user = form.get_user()
        selected_branch = form.cleaned_data.get('branch')
        # vérifier si l'utilisateur a des succursales assignées
        if not user.assigned_branches.exists():
            messages.error(self.request, "Vous n'êtes assigné à aucune succursale.")
            return redirect('login')

        # Vérifier si la succursale sélectionnée est assignée à l'utilisateur
        if selected_branch and selected_branch not in user.assigned_branches.all():
            messages.error(self.request, "Vous n'avez pas accès à cette succursale.")
            return redirect("login")

        # Enregistrer la succursale choisie dans la session
        if selected_branch:
            self.request.session['branch_id'] = selected_branch.id
            self.request.session['branch_name'] = selected_branch.description

        # vérifier l'option remember me
        if form.cleaned_data.get('remember_me'):
            # prolonger la session si "remember me est activé"
            self.request.session.set_expiry(604800)  # une semaine en seconde
        else:
            self.request.session.set_expiry(0)  # la session expirera à la fermeture du navigateur

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le nom d'utilisateur ou le mot de passe est incorrect ou le compte est inactif")

        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        # messages.success(request, "Vous avez été déconnecté(e) avec succès")
        return redirect('login')


@login_required()
def slidemenu(request):
    slides = Slides.objects.all()
    return render(request, 'slidemenu.html', {"slides": slides})
