from django.db import models
from django.conf import settings


class ApplianceCategory(models.Model):
    name = models.CharField(max_length=10)
    minimum_operating_hours = models.PositiveIntegerField()
    maximum_operating_hours = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Appliance(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(ApplianceCategory, on_delete=models.DO_NOTHING)
    power = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class HomeProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    appliances = models.ManyToManyField(Appliance)
    total_energy_consumption = models.IntegerField()  # in kWh

    @property
    def total_energy_consumption_in_watts_hours(self):
        return self.total_energy_consumption * 1000
