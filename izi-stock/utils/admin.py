from django.contrib import admin
from .models import *


@admin.register(Slides)
class SlidesAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', ]


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo','texte' ]


@admin.register(Izisoft)
class IzisoftAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo',]
