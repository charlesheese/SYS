from rest_framework import serializers

from . models import Product, User, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID', 'username', 'email']

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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'