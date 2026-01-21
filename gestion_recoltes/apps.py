from django.apps import AppConfig


class GestionRecoltesConfig(AppConfig):
    name = 'gestion_recoltes'

def ready(self):
    import gestion_recoltes.signals    
