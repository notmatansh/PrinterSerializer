from django.db import models


class Printer(models.Model):
    # Name of the Printer
    name = models.CharField(max_length=100, unique=True)
    # minimum time (in minutes) the printer needs to produce a part
    min_production_time = models.IntegerField()
    # maximum time (in minutes) the printer needs to produce a part
    max_production_time = models.IntegerField()

    def __str__(self):
        return 'printer: %s' % self.name

Printer.objects.update()