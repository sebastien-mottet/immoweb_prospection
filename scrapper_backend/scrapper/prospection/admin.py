from django.contrib import admin

from .models import ProspectionRule, ProspectionLog


@admin.register(ProspectionRule)
class ProspectionRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'has_agency', 'delay')


@admin.register(ProspectionLog)
class ProspectionLogAdmin(admin.ModelAdmin):
    list_display = ('rule', 'property')
