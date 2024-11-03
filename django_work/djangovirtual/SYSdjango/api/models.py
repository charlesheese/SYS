from django.db import models

# Create your models here.
class Product(models.Model):
    productID = models.IntegerField()
    title = models.CharField(null = False, blank  = False, max_length = 2010)
    sellerID = models.IntegerField()
    price = models.DecimalField(max_digits= 6, null = False, blank = False, decimal_places = 2)
    createdAtProduct = models.CharField(null = False, blank  = False, max_length = 2010)

def __str__(self):
    return self.title

class User(models.Model):
    userID = models.IntegerField()
    username = models.CharField(null=False, blank=False, max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    createdAt = models.DateField(null=False, blank=False)