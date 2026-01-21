from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestion_membres.models import User
from gestion_recoltes.models import Recolte
from gestion_stock.models import Stock

@login_required
def dashboard_view(request):
    user = request.user
    
    # --- LOGIQUE POUR L'ADMINISTRATEUR ---
    if user.role == 'ADMIN' or user.is_staff:
        # L'admin voit TOUT
        total_recoltes = Recolte.objects.all().count()
        tous_les_stocks = Stock.objects.all().order_by('type_produit')  # Correction : utilisation de 'type_produit' au lieu de 'produit'
        derniere_recoltes = Recolte.objects.all().order_by('-date_recolte')[:10]
        liste_producteurs = User.objects.filter(role='PRODUCTEUR')
        
        context = {
            'total_recoltes': total_recoltes,
            'stocks': tous_les_stocks,
            'recoltes': derniere_recoltes,
            'producteurs': liste_producteurs,
            'statut': "Administrateur"
        }
        return render(request, 'tableau_de_bord/dashboard_admin.html', context)

    # --- LOGIQUE POUR LE PRODUCTEUR ---
    else:
        # Le producteur ne voit que SES données
        mes_recoltes = Recolte.objects.filter(producteur=user).order_by('-date_recolte')
        
        context = {
            'recoltes': mes_recoltes,
            'statut': "Producteur"
        }
        return render(request, 'tableau_de_bord/dashboard_producteur.html', context)