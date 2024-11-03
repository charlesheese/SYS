import csv
from django.core.management.base import BaseCommand
from ..api.models import Product, User  

class Command(BaseCommand):
    help = 'Load data from CSV files'

    def handle(self, *args, **kwargs):
        # Load Products
        with open('../../../../mock_data/Products.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                product = Product(
                    productID = row['productId'],
                    title=row['title'],
                    price=row['price'],
                    sellerId=row['sellerId'],
                    createdAt=row['Created_at']
                )
                product.save()

        # Load Users
        with open('../../../../mock_data/Users.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user = User(
                    userID=row['Id'],
                    username=row['User_name'],
                    email=row['email'],
                    password=row['password'],  ##### HASH IN THE FUTURE *****MUST
                    createdAt=row['Year_of_graduation']
                )
                user.save()

        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
