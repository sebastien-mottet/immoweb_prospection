from django.db import models

from properties.models import Property


class ProspectionRule(models.Model):

    name = models.CharField(max_length=200)
    has_agency = models.BooleanField(default=False)
    delay = models.SmallIntegerField(default=0)
    message = models.TextField()

    class Meta:
        verbose_name = 'prospection rule'
        verbose_name_plural = 'prospection rules'


class ProspectionLog(models.Model):

    rule = models.ForeignKey(ProspectionRule, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'prospection log'
        verbose_name_plural = 'prospection logs'
