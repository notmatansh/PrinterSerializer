from django.db import models


class Printer(models.Model):
    """
    the given model for the practice
    """
    # Name of the Printer
    name = models.CharField(max_length=100)
    # minimum time (in minutes) the printer needs to produce a part
    min_production_time = models.IntegerField()
    # maximum time (in minutes) the printer needs to produce a part
    max_production_time = models.IntegerField()

    def __str__(self):
        return 'printer: %s' % self.name


class Contact(models.Model):
    """
    another data model meant to test out more complex scenarios like unique fields and multi-layered nesting
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=30, unique=True)
    city = models.CharField(max_length=300)
    street = models.CharField(max_length=300)
    house_number = models.IntegerField()
    apartment_floor = models.IntegerField(default=0)
    house_entrance = models.CharField(max_length=10, blank=True)
    apartment_number = models.IntegerField()

    def __str__(self):
        return '%s %s' % (self.first_name.capitalize(), self.last_name.capitalize())
