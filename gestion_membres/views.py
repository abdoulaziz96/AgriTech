from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

### Pour les statistiques avancées
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import json
from .models import User

# Imports de tes modèles
from .models import User
from .forms import InscriptionProducteurForm
from gestion_recoltes.models import Recolte, Parcelle  # Importé depuis l'autre application

# ==========================================
# 1. AUTHENTIFICATION ET CONNEXION
# ==========================================

def login_view(request):
    """Vue de connexion avec redirection par rôle"""
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None:
            login(request, user)
            # Redirection selon le rôle défini dans le modèle User
            if user.role == 'ADMIN' or user.is_superuser:
                return redirect('/admin/')
            elif user.role == 'GESTIONNAIRE':
                return redirect('dashboard_gestionnaire')
            elif user.role == 'PRODUCTEUR':
                return redirect('gestion:dashboard_producteur')
            else:
                return redirect('accueil')
        else:
            return render(request, 'gestion_membres/login.html', {'error': True})
            
    return render(request, 'gestion_membres/login.html')

def register_view(request):
    """Inscription pour les nouveaux producteurs"""
    if request.method == 'POST':
        form = InscriptionProducteurForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'PRODUCTEUR'
            user.save()
            messages.success(request, "Compte créé ! Connectez-vous.")
            return redirect('login')
    else:
        form = InscriptionProducteurForm()
    return render(request, 'gestion_membres/register.html', {'form': form})

# ==========================================
# 2. VUES DES TABLEAUX DE BORD (DASHBOARDS)
# ==========================================

@login_required
def dashboard_producteur(request):
    """Tableau de bord spécifique au producteur"""
    if request.user.role != 'PRODUCTEUR':
        return redirect('accueil')
    
    # On récupère les récoltes liées aux parcelles du producteur connecté
    recoltes = Recolte.objects.filter(producteur=request.user)
    return render(request, 'gestion_membres/dashboard_producteur.html', {'recoltes': recoltes})

@login_required
def dashboard_gestionnaire(request):
    """Tableau de bord spécifique au gestionnaire"""
    if request.user.role != 'GESTIONNAIRE':
        return redirect('accueil')
    return render(request, 'gestion_membres/dashboard_gestionnaire.html')

# ==========================================
# 3. AUTRES VUES
# ==========================================

def accueil_view(request):
    return render(request, 'gestion_membres/accueil.html')

@login_required
def detail_parcelle(request, parcelle_id):
    # On cherche la parcelle dans l'application gestion_recoltes
    parcelle = get_object_or_404(Parcelle, id=parcelle_id)
    return render(request, 'gestion_membres/detail_parcelle.html', {'parcelle': parcelle})

@login_required
def liste_producteurs(request):
    producteurs = User.objects.filter(role='PRODUCTEUR')
    return render(request, 'gestion_membres/liste_producteurs.html', {'producteurs': producteurs})



def is_admin_or_gestionnaire(user):
    """Vérifie si l'utilisateur a accès au dashboard"""
    return user.is_staff or user.is_superuser or user.role in ['ADMIN', 'GESTIONNAIRE']

@login_required
@user_passes_test(is_admin_or_gestionnaire)
def admin_dashboard(request):
    """Vue du tableau de bord administrateur"""
    
    # 1. STATISTIQUES DES UTILISATEURS
    total_users = User.objects.count()
    total_producteurs = User.objects.filter(role='PRODUCTEUR').count()
    total_gestionnaires = User.objects.filter(role='GESTIONNAIRE').count()
    total_admins = User.objects.filter(role='ADMIN').count()
    
    # Utilisateurs actifs aujourd'hui
    aujourdhui = timezone.now().date()
    utilisateurs_actifs = User.objects.filter(last_login__date=aujourdhui).count()
    
    # Nouveaux utilisateurs (7 derniers jours)
    sept_jours = timezone.now() - timedelta(days=7)
    nouveaux_utilisateurs = User.objects.filter(date_joined__gte=sept_jours).count()
    
    # 2. STATISTIQUES PAR LOCALITÉ (si champ localite existe)
    stats_localites = User.objects.filter(
        localite__isnull=False
    ).exclude(
        localite=''
    ).values('localite').annotate(
        count=Count('id'),
        producteurs=Count('id', filter=Q(role='PRODUCTEUR')),
        gestionnaires=Count('id', filter=Q(role='GESTIONNAIRE'))
    ).order_by('-count')[:10]
    
    # 3. ACTIVITÉ RÉCENTE
    # Derniers utilisateurs inscrits
    derniers_inscrits = User.objects.order_by('-date_joined')[:10]
    
    # Dernières connexions
    dernieres_connexions = User.objects.filter(
        last_login__isnull=False
    ).order_by('-last_login')[:10]
    
    # 4. GRAPHIQUES - Évolution des inscriptions
    inscriptions_data = []
    for i in range(30, -1, -1):  # 31 derniers jours
        date = aujourdhui - timedelta(days=i)
        count = User.objects.filter(date_joined__date=date).count()
        inscriptions_data.append({
            'date': date.strftime('%d/%m'),
            'count': count
        })
    
    # 5. RÉPARTITION PAR RÔLE
    repartition_roles = []
    for role_code, role_name in User.ROLE_CHOICES:
        count = User.objects.filter(role=role_code).count()
        if count > 0:
            percentage = (count / total_users * 100) if total_users > 0 else 0
            repartition_roles.append({
                'role': role_name,
                'code': role_code,
                'count': count,
                'percentage': round(percentage, 1)
            })
    
    # 6. DONNÉES POUR GRAPHIQUES
    chart_data = {
        'inscriptions': {
            'labels': [item['date'] for item in inscriptions_data],
            'data': [item['count'] for item in inscriptions_data]
        },
        'repartition': {
            'labels': [item['role'] for item in repartition_roles],
            'data': [item['count'] for item in repartition_roles],
            'backgroundColors': [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
                '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
            ]
        }
    }
    
    # 7. ALERTES ET NOTIFICATIONS
    alertes = []
    
    # Exemple: Vérifier les utilisateurs sans rôle spécifié
    users_sans_role_specifique = User.objects.filter(role='PRODUCTEUR', telephone__isnull=True)
    if users_sans_role_specifique.exists():
        alertes.append({
            'type': 'warning',
            'message': f'{users_sans_role_specifique.count()} producteurs sans téléphone',
            'icon': 'phone'
        })
    
    # 8. PERFORMANCE DU SYSTÈME
    temps_debut = timezone.now()
    # Simulation de temps de réponse
    import time
    time.sleep(0.1)  # Simulation
    
    context = {
        # Métadonnées
        'page_title': 'Tableau de Bord Administratif',
        'user': request.user,
        'now': timezone.now(),
        
        # Statistiques principales
        'total_users': total_users,
        'total_producteurs': total_producteurs,
        'total_gestionnaires': total_gestionnaires,
        'total_admins': total_admins,
        'utilisateurs_actifs': utilisateurs_actifs,
        'nouveaux_utilisateurs': nouveaux_utilisateurs,
        
        # Données détaillées
        'stats_localites': stats_localites,
        'derniers_inscrits': derniers_inscrits,
        'dernieres_connexions': dernieres_connexions,
        'repartition_roles': repartition_roles,
        'inscriptions_data': inscriptions_data,
        
        # Pour JavaScript
        'chart_data_json': json.dumps(chart_data),
        
        # Alertes
        'alertes': alertes,
        
        # Performance
        'temps_chargement': round((timezone.now() - temps_debut).total_seconds() * 1000, 2),
    }
    
    return render(request, 'admin/dashboard.html', context)