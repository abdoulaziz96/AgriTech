from django.db import models
from django.conf import settings

class Parcelle(models.Model):
    nom = models.CharField(max_length=100)
    superficie = models.DecimalField(max_digits=10, decimal_places=2)
    producteur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='parcelles'
    )

    def __str__(self):
        return f"{self.nom} - {self.producteur.username}"

class Recolte(models.Model):
    CULTURES = [
        ('MAIS', 'Maïs'), ('SOJA', 'Soja'), 
        ('ANANAS', 'Ananas'), ('RIZ', 'Riz'),
    ]
    producteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    type_culture = models.CharField(max_length=20, choices=CULTURES)
    quantite_kg = models.DecimalField(max_digits=10, decimal_places=2)
    date_recolte = models.DateField(auto_now_add=True)
    est_valide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type_culture} ({self.quantite_kg}kg) - {self.producteur.username}"