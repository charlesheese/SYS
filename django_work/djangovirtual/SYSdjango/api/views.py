from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token  # Token Authentication
from .serializer import ProductSerializer, UserSerializer, UserRegisterSerializer, UserLoginSerializer
from .models import Product, User
from django.db.models import Q

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
        'User Register': '/register/',
        'User Login': '/login/',
    }
    return Response(api_urls)

class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Product Views
@api_view(['GET'])
def ShowAll(request):
    products = Product.objects.all()
    is_sold = request.query_params.get('is_sold')
    if is_sold is not None:
        products = products.filter(is_sold=is_sold.lower() == 'true')

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

# Registration and Login Views
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key, "message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



