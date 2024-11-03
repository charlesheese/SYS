import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from ..api.models import Product, User  

class Command(BaseCommand):
    help = 'Load data from CSV files'

    def handle(self, *args, **kwargs):
        # Load Products
        with open('../../../../mock_data/Products.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                created_at_product = datetime.strptime(row['Created_at'], '%m/%d/%Y').date()
                
                product = Product(
                    productID=row['productId'],
                    title=row['title'],
                    price=row['price'],
                    sellerId=row['sellerId'],
                    createdAtProduct=created_at_product
                )
                product.save()

        # Load Users
        with open('../../../../mock_data/Users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert Year_of_graduation to a full datetime, assuming January 1st, 00:00:00
                graduation_year = int(row['Year_of_graduation'])
                created_at = datetime(graduation_year, 1, 1, 0, 0, 0)

                user = User(
                    userID=row['Id'],
                    username=row['User_name'],
                    email=row['email'],
                    password=row['password'],  # REMEMBER TO HASH IN THE FUTURE
                    createdAt=created_at
                )
                user.save()

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))


