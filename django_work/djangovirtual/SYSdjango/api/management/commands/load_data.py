import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import User, Product

class Command(BaseCommand):
    help = 'Load user and product data from CSV files'

    def handle(self, *args, **kwargs):
        # Load Users
        user_file_path = os.path.join(os.path.dirname(__file__), '/Users/aryamanwade/SYS/django_work/djangovirtual/SYSdjango/api/mock_data/Users.csv')
        
        with open(user_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    created_at = datetime.strptime(row['createdAt'], '%m/%d/%Y').date()
                except ValueError:
                    created_at = datetime.strptime(row['createdAt'], '%m/%d/%Y').date()

                user = User(
                    userID=int(row['userID']),
                    username=row['username'],
                    email=row['email'],
                    password=row['password'],
                    createdAt=created_at
                )
                user.save()
        
        self.stdout.write(self.style.SUCCESS('User data loaded successfully.'))

        # Load Products
        product_file_path = os.path.join(os.path.dirname(__file__), '/Users/aryamanwade/SYS/django_work/djangovirtual/SYSdjango/api/mock_data/Products.csv')

        with open(product_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                created_at_product = datetime.strptime(row['createdAtProduct'], '%m/%d/%Y').date()

                product = Product(
                    productID=int(row['productID']),
                    title=row['title'],
                    sellerID=int(row['sellerID']),
                    price=float(row['price']),
                    createdAtProduct=created_at_product
                )
                product.save()

        self.stdout.write(self.style.SUCCESS('Product data loaded successfully.'))


