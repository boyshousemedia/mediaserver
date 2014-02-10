from django.contrib import admin
from django.db import models


class Disk(models.Model):
    name = models.CharField(max_length=50)
    capacity_terabytes = models.FloatField()
    available_terabytes = models.FloatField()

    def __unicode__(self):
        return self.name


admin.site.register(Disk)