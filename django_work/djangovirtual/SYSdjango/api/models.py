from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    productID = models.IntegerField(unique=True, null=True, blank=True)  # Temporary change to nullable
    title = models.CharField(null=False, blank=False, max_length=255)
    sellerID = models.IntegerField(null=True, blank=True)  # Temporary change to nullable
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    createdAtProduct = models.DateField(null=False, blank=False)
    is_sold = models.BooleanField(default=False)

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
    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.timestamp}"