from django.db import models


# Create your models here.
class Price(models.Model):
    date = models.DateField()
    time = models.IntegerField()

    values = models.FloatField()

    class Meta:
        verbose_name = "price"
