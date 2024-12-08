from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Product, User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Changed userID to id for the default primary key

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        # Validate the email field
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError({"email": "This field is required."})
        if not email.endswith('@northeastern.edu'):
            raise serializers.ValidationError({"email": "Email must be a northeastern.edu address."})

        return attrs

    # Remove the 'create' method to defer saving until after verification



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Use `authenticate` to log in with email instead of username
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        data['user'] = user
        return data



class ProductSerializer(serializers.ModelSerializer):
    # Define a field to retrieve the seller's information
    seller = UserSerializer(read_only=True)  # Use UserSerializer directly for the seller

    class Meta:
        model = Product
        fields = ['productID', 'title', 'price', 'created_at', 'is_sold', 'seller']


