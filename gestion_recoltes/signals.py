from django.db.models.signals import post_save
from django.dispatch import receiver
from gestion_recoltes.models import Recolte
from gestion_stock.models import Stock

@receiver(post_save, sender=Recolte)
def mettre_a_jour_stock(sender, instance, created, **kwargs):
    if created:
        # On récupère ou on crée la ligne de stock pour ce produit
        stock, _ = Stock.objects.get_or_create(type_produit=instance.type_culture)
        # On ajoute la nouvelle récolte au cumul
        stock.quantite_totale += instance.quantite_kg
        stock.save()