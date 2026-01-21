from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('GESTIONNAIRE', 'Gestionnaire'),
        ('PRODUCTEUR', 'Producteur'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PRODUCTEUR')
    telephone = models.CharField(max_length=15, blank=True, null=True)
    localite = models.CharField(max_length=100, blank=True, null=True)
    
    # Ajoutez ces champs si vous en avez besoin
    commune = models.CharField(max_length=100, blank=True, null=True)
    arrondissement = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"