from stocks.models import *
from utils.models import *


def current_branch(request):
    """cette fonction récupère la succursale à laquelle l'utilisateur s'est connecté
    et l'affiche dans le sidebar
    """
    if request.user.is_authenticated:
        branch_id = request.session.get('branch_id')
        branch = Branch.objects.filter(id=branch_id).first() if branch_id else None
        return {'current_branch': branch}
    return {'current_branch': None}


def entreprise_logo(request):
    """récupérer le logo et le nom de l'entreprise"""
    entreprise_logo = Entreprise.objects.first()

    return {'entreprise_logo':entreprise_logo}