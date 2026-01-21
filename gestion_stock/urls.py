from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.liste_stocks, name='liste_stocks'),
    path('stock/<int:stock_id>/', views.detail_stock, name='detail_stock'),
]