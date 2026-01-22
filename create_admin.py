import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ton_projet.settings') # Remplace 'ton_projet' par le nom de ton dossier settings
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin1'
password = '1234567890' # Change ce mot de passe !

if not User.objects.filter(username=username).exists():
    print(f"Création du superutilisateur {username}...")
    User.objects.create_superuser(username, email, password)
    print("Superutilisateur créé avec succès !")
else:
    print("Le superutilisateur existe déjà.")