from django.db import models


class Search(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'search'
        verbose_name_plural = 'searches'
