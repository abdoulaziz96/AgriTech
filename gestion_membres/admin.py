from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'commune', 'arrondissement', 'is_staff', 'is_active')  # Ajout des champs commune et arrondissement
    list_filter = ('role', 'commune', 'arrondissement', 'is_staff', 'is_superuser')  # Ajout des champs commune et arrondissement

    # Configuration des formulaires (Ajout des champs commune et arrondissement)
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations AgriTech', {'fields': ('role', 'telephone', 'localite', 'commune', 'arrondissement')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informations AgriTech', {'fields': ('role', 'telephone', 'localite', 'commune', 'arrondissement')}),
    )