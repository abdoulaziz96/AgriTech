import os
import django
import sys

# 1. Détection automatique du dossier de configuration (settings)
def find_settings_module():
    # Cherche un dossier qui contient 'settings.py'
    for root, dirs, files in os.walk('.'):
        if 'settings.py' in files:
            # On transforme le chemin en format module (ex: AgriTech_Benin.settings)
            module_path = root.replace(os.sep, '.').strip('.')
            return f"{module_path}.settings"
    return None

settings_module = find_settings_module()

if settings_module:
    print(f"--- Configuration détectée : {settings_module} ---")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    django.setup()
else:
    print("ERREUR : Impossible de trouver le fichier settings.py")
    sys.exit(1)

from django.contrib.auth import get_user_model

# 2. Création du compte
User = get_user_model()
username = 'admin_agri'
email = 'admin1'
password = '1234567890' # Change-le après ta première connexion !

try:
    if not User.objects.filter(username=username).exists():
        print(f"Création du superutilisateur {username}...")
        User.objects.create_superuser(username, email, password)
        print("✅ Superutilisateur créé avec succès !")
    else:
        print(f"ℹ️ L'utilisateur {username} existe déjà.")
except Exception as e:
    print(f"❌ Erreur lors de la création : {e}")