from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stock

@login_required
def liste_stocks(request):
    stocks = Stock.objects.all()
    return render(request, 'gestion_stock/liste_stocks.html', {'stocks': stocks})

@login_required
def detail_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    return render(request, 'gestion_stock/detail_stock.html', {'stock': stock})
