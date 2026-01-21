from django import forms
from .models import Recolte

class RecolteForm(forms.ModelForm):
    class Meta:
        model = Recolte
        fields = ['parcelle', 'type_culture', 'quantite_kg']
        widgets = {
            'parcelle': forms.Select(attrs={'class': 'form-control'}),
            'type_culture': forms.Select(attrs={'class': 'form-control'}),
            'quantite_kg': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 500'}),
        }