from django.db import models


class Property(models.Model):
    immoweb_code = models.IntegerField(primary_key=True)
    has_agency = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.immoweb_code)

    class Meta:
        verbose_name = 'property'
        verbose_name_plural = 'properties'
