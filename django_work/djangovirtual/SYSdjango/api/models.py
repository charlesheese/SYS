from django.db import models
from django.utils import timezone


# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Product(models.Model):
    productID = models.IntegerField(unique=True, null=True, blank=True)  # Temporary change to nullable
    title = models.CharField(null=False, blank=False, max_length=255)
    sellerID = models.IntegerField(null=True, blank=True)  # Temporary change to nullable
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    createdAtProduct = models.DateField(null=False, blank=False)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
