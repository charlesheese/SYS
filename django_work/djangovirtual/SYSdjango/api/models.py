from django.db import models

# Create your models here.
class Product(models.Model):
    idnum = models.IntegerField()
    title = models.CharField(null = False, blank  = False, max_length = 2010)
    sellerId = models.IntegerField()
    price = models.DecimalField(max_digits= 6, null = False, blank = False, decimal_places = 2)
    createdAt = models.DateTimeField()

def __str__(self):
    return self.idnnum