import os
import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):
    help = 'Load user data from CSV file'

    def handle(self, *args, **kwargs):
        # Absolute path to mock_data/Users.csv
        file_path = os.path.join(os.path.dirname(__file__), '/Users/aryamanwade/SYS/django_work/djangovirtual/SYSdjango/api/mock_data/Users.csv')
        
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    created_at = datetime.strptime(row['createdAt'], '%m/%d/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    created_at = datetime.strptime(row['createdAt'], '%m/%d/%Y').strftime('%Y-%m-%d')

                user = User(
                    userID=int(row['userID']),
                    username=row['username'],
                    email=row['email'],
                    password=row['password'],
                    createdAt=created_at
                )
                user.save()

        self.stdout.write(self.style.SUCCESS('User data loaded successfully.'))

