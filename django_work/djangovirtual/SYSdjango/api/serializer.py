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
    verification_code = serializers.CharField(write_only=True, required=True) 
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'verification_code']

    def validate(self, attrs):
        # Validate the email field
        email = attrs.get('email')
        if not email:
            raise serializers.ValidationError({"email": "This field is required."})
        if not email.endswith('@northeastern.edu'):
            raise serializers.ValidationError({"email": "Email must be a northeastern.edu address."})
        
        code = attrs.get('verification_code')
        if code != '1234':  # Static code for now
            raise serializers.ValidationError({"verification_code": "Invalid verification code"})
        
        # Return the validated attributes
        return attrs

    def create(self, validated_data):
        # Create a new user and hash the password
        validated_data['email'] = validated_data['email'].lower()
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        validated_data.pop('verification_code', None)
        user.set_password(validated_data['password'])
        user.save()
        return user

# New serializer for user login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ProductSerializer(serializers.ModelSerializer):
    # Define a field to retrieve the seller's information
    seller = UserSerializer(read_only=True)  # Use UserSerializer directly for the seller

    class Meta:
        model = Product
        fields = ['productID', 'title', 'price', 'created_at', 'is_sold', 'seller']


