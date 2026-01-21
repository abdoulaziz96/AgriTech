# gestion_recoltes/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RecolteForm


@login_required
def ajouter_recolte(request):
    if request.method == 'POST':
        form = RecolteForm(request.POST)
        if form.is_valid():
            recolte = form.save(commit=False)
            # On lie automatiquement la récolte à l'utilisateur connecté
            recolte.producteur = request.user
            recolte.save()
            messages.success(request, "Votre récolte a été enregistrée avec succès !")
            return redirect('dashboard')
    else:
        form = RecolteForm()
        # Sécurité : Le producteur ne voit que ses propres parcelles dans la liste
        form.fields['parcelle'].queryset = request.user.parcelle_set.all()
    
    return render(request, 'gestion_recoltes/ajouter_recolte.html', {'form': form})

def ajouter_recolte(request):
    # Pour l'instant, on affiche juste une page simple
    return render(request, 'gestion_recoltes/ajouter_recolte.html')