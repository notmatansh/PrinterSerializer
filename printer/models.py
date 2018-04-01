from django.db import models


class Printer(models.Model):
    # Name of the Printer
    name = models.CharField(max_length=100)
    # minimum time (in minutes) the printer needs to produce a part
    min_production_time = models.IntegerField()
    # maximum time (in minutes) the printer needs to produce a part
    max_production_time = models.IntegerField()

    def __str__(self):
        return 'printer: %s' % self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=30, unique=True)
    city = models.CharField(max_length=300)
    street = models.CharField(max_length=300)
    house_number = models.IntegerField()
    apartment_number = models.IntegerField()

    def __str__(self):
        return '%s %s' % (self.first_name.capitalize(), self.last_name.capitalize())
