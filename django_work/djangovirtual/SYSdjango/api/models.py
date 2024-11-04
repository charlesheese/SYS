from django.db import models

# Create your models here.
class Product(models.Model):
    productID = models.IntegerField(unique=True)  # Makes productID unique to avoid duplicates
    title = models.CharField(null=False, blank=False, max_length=255)  # Reduced max length for title
    sellerID = models.IntegerField()  # Assuming this is an ID, IntegerField is fine
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    createdAtProduct = models.DateTimeField(null=False, blank=False)  # Changed to DateTimeField for date storage


def __str__(self):
    return self.title

class User(models.Model):
    userID = models.IntegerField(primary_key=True)
    username = models.CharField(null=False, blank=False, max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    createdAt = models.DateField(null=False, blank=False)

def __str__(self):
    return self.username