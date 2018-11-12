from django.db import models


class Continent(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    code = models.CharField(max_length = 2, unique = True)
    class Meta:
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    capital = models.CharField(max_length = 255)
    code = models.CharField(max_length = 2, unique = True)
    population = models.PositiveIntegerField()
    area = models.PositiveIntegerField()
    continent = models.ForeignKey('Continent', on_delete = models.CASCADE, related_name = 'countries')
    class Meta:
        ordering = ['name']