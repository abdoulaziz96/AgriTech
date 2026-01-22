import os
from pathlib import Path
import dj_database_url

# ==================================================
# BASE DIR
# ==================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# ENVIRONNEMENT (LOCAL / RENDER)
# ==================================================
IS_RENDER = (
    'RENDER' in os.environ
    or 'RENDER_EXTERNAL_HOSTNAME' in os.environ
)

# ==================================================
# SECURITY
# ==================================================
if IS_RENDER:
    print("🌐 ENVIRONNEMENT: RENDER (Production)")

    DEBUG = False

    ALLOWED_HOSTS = [
        'agritech-benin-xnrh.onrender.com',
        '.onrender.com',
    ]

    SECRET_KEY = (
        os.environ.get('SECRET_KEY')
        or os.environ.get('DJANGO_SECRET_KEY')
        or os.environ.get('RENDER_SECRET_KEY')
    )

    if not SECRET_KEY:
        raise ValueError("❌ SECRET_KEY manquante sur Render")

else:
    print("💻 ENVIRONNEMENT: DÉVELOPPEMENT LOCAL")

    DEBUG = True

    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
    ]

    SECRET_KEY = 'django-insecure-dev-key-local-only-change-me'

print(f"✅ DEBUG: {DEBUG}")
print(f"✅ ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# ==================================================
# APPLICATIONS (✅ CORRIGÉ)
# ==================================================
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Applications du projet (⚠️ OBLIGATOIRE)
    'gestion_membres',
    'gestion_recoltes',
    'gestion_stock',
    'tableau_de_bord',
]

# ==================================================
# USER PERSONNALISÉ
# ==================================================
AUTH_USER_MODEL = 'gestion_membres.User'

# ==================================================
# MIDDLEWARE
# ==================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================================================
# URLS & WSGI
# ==================================================
ROOT_URLCONF = 'core_settings.urls'
WSGI_APPLICATION = 'core_settings.wsgi.application'

# ==================================================
# TEMPLATES
# ==================================================
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

# ==================================================
# DATABASE
# ==================================================
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600,
        ssl_require=IS_RENDER
    )
}

# ==================================================
# PASSWORD VALIDATION
# ==================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==================================================
# INTERNATIONALIZATION
# ==================================================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

# ==================================================
# STATIC FILES
# ==================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ==================================================
# DEFAULT PRIMARY KEY
# ==================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
