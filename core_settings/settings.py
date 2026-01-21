import os
from pathlib import Path
import dj_database_url

# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# DEBUG - À TOUJOURS METTRE EN PREMIER
# =========================
print("=" * 60)
print("🚀 INITIALISATION DJANGO")
print("=" * 60)

# =========================
# DÉTECTION SIMPLE DE L'ENVIRONNEMENT
# =========================
# Méthode 100% fiable : vérifie si on a une DATABASE_URL Render
IS_RENDER = 'postgresql' in os.environ.get('DATABASE_URL', '')

if IS_RENDER:
    print("🌐 ENVIRONNEMENT: RENDER (Production)")
    # Configuration Render
    DEBUG = False
    ALLOWED_HOSTS = [
        'agritech-benin-xnrh.onrender.com',
        '.onrender.com',
    ]
    # SECRET_KEY doit ABSOLUMENT être définie sur Render
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("❌ ERREUR: SECRET_KEY manquante sur Render!")
    
else:
    print("💻 ENVIRONNEMENT: DÉVELOPPEMENT LOCAL")
    # Configuration locale
    DEBUG = True
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '127.0.0.1:8000',
        '0.0.0.0',
        '[::1]',
    ]
    SECRET_KEY = 'django-insecure-dev-key-local-only-change-me'

print(f"✅ DEBUG: {DEBUG}")
print(f"✅ ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"✅ SECRET_KEY: {'DÉFINIE' if SECRET_KEY else '❌ MANQUANTE'}")

# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',

    'gestion_membres',
    'gestion_recoltes',
    'gestion_stock',
    'tableau_de_bord',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core_settings.urls'
WSGI_APPLICATION = 'core_settings.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =========================
# DATABASE - SIMPLIFIÉ
# =========================
if IS_RENDER:
    print("📦 DATABASE: PostgreSQL (Render)")
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    print("📦 DATABASE: SQLite (Local)")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# INTERNATIONALISATION
# =========================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# SECURITY SETTINGS
# =========================
if IS_RENDER:
    print("🔒 SÉCURITÉ: Mode production")
    CSRF_TRUSTED_ORIGINS = [
        'https://agritech-benin-xnrh.onrender.com',
        'https://*.onrender.com',
    ]
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    print("🔓 SÉCURITÉ: Mode développement")
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# =========================
# AUTHENTIFICATION
# =========================
AUTH_USER_MODEL = 'gestion_membres.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# =========================
# DEFAULT PK
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

print("=" * 60)
print("✅ CONFIGURATION CHARGÉE AVEC SUCCÈS")
print("=" * 60)