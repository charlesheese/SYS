from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
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


class User(AbstractBaseUser, PermissionsMixin):
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
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Product(models.Model):
    productID = models.AutoField(primary_key=True)  # Auto-generated unique ID
    title = models.CharField(max_length=255, null=True, blank=True)  # Optional title
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # Set seller to NULL if the user is deleted
        related_name="products",
        null=True,
        blank=True  # Allow seller to be optional
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional price
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Auto set at creation, optional
    is_sold = models.BooleanField(default=False, null=True, blank=True)  # Optional with default value

    def __str__(self):
        return f"{self.title or 'Untitled Product'} - ${self.price or 'N/A'}"
    
class VerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} - {self.code}'
