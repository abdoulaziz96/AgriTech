# gestion_recoltes/urls.py

from django.urls import path
from . import views

app_name = 'gestion_recoltes'

urlpatterns = [
    path('ajouter/', views.ajouter_recolte, name='ajouter_recolte'),
]# gestion_recoltes/urls.py

from django.urls import path
from . import views

app_name = 'gestion_recoltes'

urlpatterns = [
    path('ajouter/', views.ajouter_recolte, name='ajouter_recolte'),
]