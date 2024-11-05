from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import ProductSerializer, UserSerializer, MessageSerializer
from .models import Product, User, Message
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

# API Overview
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Product List': '/product-list/',
        'Product Detail View': '/product-detail/<int:id>',
        'Product Create': '/product-create/',
        'Product Update': '/product-update/<int:id>',
        'Product Delete': '/product-delete/<int:id>',
        'User List': '/user-list/',
        'User Detail View': '/user-detail/<int:id>',
        'User Create': '/user-create/',
        'User Update': '/user-update/<int:id>',
        'User Delete': '/user-delete/<int:id>',
        'Message List': '/message-list/<int:sender_id>/<int:recipient_id>/',
        'Message Create': '/message-create/',
    }
    return Response(api_urls)

class ProductPagination(PageNumberPagination):
    page_size = 10  # Number of products per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Optional: limits the maximum items per page

# Product Views
@api_view(['GET'])
def ShowAll(request):
    products = Product.objects.all()
    
    # Filter by is_sold status if provided in query parameters
    is_sold = request.query_params.get('is_sold')
    if is_sold is not None:
        products = products.filter(is_sold=is_sold.lower() == 'true')

    # Apply pagination
    paginator = ProductPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def ViewProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def CreateProduct(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def UpdateProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(instance=product, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def DeleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return Response('Product deleted successfully')

# User Views
@api_view(['GET'])
def ShowAllUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ViewUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def CreateUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def UpdateUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def DeleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response('User deleted successfully')

def ShowMessagesBetweenUsers(request, sender_id, recipient_id):
    # Retrieve all messages between two users, ordered by timestamp
    messages = Message.objects.filter(
        (Q(sender_id=sender_id) & Q(recipient_id=recipient_id)) |
        (Q(sender_id=recipient_id) & Q(recipient_id=sender_id))
    ).order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def CreateMessage(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
