
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from gestion_membres.views import accueil_view, login_view, register_view
from gestion_membres.views import admin_dashboard

urlpatterns = [
     # IMPORTANT: Définissez vos URLs PERSONNALISÉES d'abord
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('', accueil_view, name='home'),  # Page d'accueil
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),

    # Apps principales
    path('gestion/', include('gestion_membres.urls')),
    path('recoltes/', include('gestion_recoltes.urls')),
    path('stock/', include('gestion_stock.urls')),
    path('dashboard/', include('tableau_de_bord.urls')),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    
    
    
]