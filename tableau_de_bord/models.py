from django.db import models

# Create your models here.

class RendementParZone(models.Model):
    zone = models.CharField(max_length=100)
    culture = models.CharField(max_length=50)
    rendement_total = models.FloatField(help_text="Rendement total en tonnes")

    def __str__(self):
        return f"{self.zone} - {self.culture} : {self.rendement_total} tonnes"
