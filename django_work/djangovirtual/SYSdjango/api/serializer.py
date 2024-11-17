from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Product, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Changed userID to id for the default primary key

# New serializer for user registration
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate_email(self, value):
        # Check if the email is a .edu address
        if not value.endswith('northeastern.edu'):
            raise serializers.ValidationError("Email must be a .northeastern.edu address")
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")
        return value

    def create(self, validated_data):
        # Create a new user and hash the password
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# New serializer for user login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ProductSerializer(serializers.ModelSerializer):
    # Define a field to retrieve the seller's information
    seller = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'productID', 'title', 'price', 'createdAtProduct', 'is_sold', 'seller']

    def get_seller(self, obj):
        # Retrieve the User associated with the sellerID if it exists
        try:
            user = User.objects.get(userID=obj.sellerID)
            return UserSerializer(user).data
        except User.DoesNotExist:
            return None  # If the user doesn't exist, return None


