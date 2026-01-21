from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    # Les colonnes à afficher dans la liste
    list_display = ('type_produit', 'quantite_totale', 'derniere_mise_a_jour')
    
    # Ajouter un champ de recherche
    search_fields = ('type_produit',)
    
    # Permettre de modifier le seuil directement depuis la liste
    list_editable = ('quantite_totale',)