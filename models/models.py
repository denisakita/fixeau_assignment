from django.db import models


class GroundWater(models.Model):
    class Meta:
        verbose_name = 'GroundWater'
        verbose_name_plural = 'GroundWaters'
        ordering = ['date', 'measurement']
        db_table = 'drf_groundwater'

    date = models.DateField()
    measurement = models.FloatField()
