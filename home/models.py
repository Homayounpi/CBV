from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    created = models.DateField(blank=True,null=True)
    def __str__(self):
        return self.name