from django.db import models

# On définit les choix ici pour éviter d'importer d'ailleurs (évite les bugs)
CHOIX_CULTURE = [
    ('MAIS', 'Maïs'),
    ('SOJA', 'Soja'),
    ('ANANAS', 'Ananas'),
    ('RIZ', 'Riz'),
]

class Stock(models.Model):
    type_produit = models.CharField(
        max_length=20, 
        choices=CHOIX_CULTURE, 
        unique=True,
        verbose_name="Type de Produit"
    )
    quantite_totale = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Quantité Totale (kg)"
    )
    derniere_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_produit_display()} : {self.quantite_totale} kg"

    class Meta:
        verbose_name = "Stock Global"
        verbose_name_plural = "Stocks Globaux"