from django import forms
from .models import Stock

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['entrepot', 'culture', 'quantite']
        labels = {
            'entrepot': 'Entrepôt',
            'culture': 'Culture',
            'quantite': 'Quantité (en tonnes)',
        }