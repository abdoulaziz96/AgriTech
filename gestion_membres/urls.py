from django.urls import path
from . import views

urlpatterns = [
    # Accueil et Authentification
    path('', views.accueil_view, name='accueil'),
    path('login/', views.login_view, name='login'), # Utilise le nom simplifié du views.py
    path('register/', views.register_view, name='register'),
    
    # Tableaux de bord (Dashboards)
    path('dashboard/producteur/', views.dashboard_producteur, name='dashboard_producteur'),
    path('dashboard/gestionnaire/', views.dashboard_gestionnaire, name='dashboard_gestionnaire'),
    
    # Gestion des membres et données
    path('producteurs/', views.liste_producteurs, name='liste_producteurs'),
    path('parcelle/<int:parcelle_id>/', views.detail_parcelle, name='detail_parcelle'),
]