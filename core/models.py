from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    user = models.ManyToManyField(User, default=None,)
    name = models.CharField(max_length=255, verbose_name="Название города")
    lat = models.CharField(max_length=20, verbose_name="Широта", default=None, null=True, blank=True)
    lon = models.CharField(max_length=20, verbose_name="Долгота", default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = 'Cities'
