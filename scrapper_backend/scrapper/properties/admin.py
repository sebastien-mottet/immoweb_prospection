from django.contrib import admin

from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('immoweb_code', 'has_agency', 'active', 'create_date')
