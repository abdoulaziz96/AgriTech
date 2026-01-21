from django.contrib import admin
from .models import Parcelle, Recolte

@admin.register(Parcelle)
class ParcelleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'producteur', 'superficie')
    search_fields = ('nom', 'producteur__username')

@admin.register(Recolte)
class RecolteAdmin(admin.ModelAdmin):
    list_display = ('type_culture', 'producteur', 'quantite_kg', 'est_valide')
    list_filter = ('type_culture', 'est_valide')