from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token  # Token Authentication
from .serializer import ProductSerializer, UserSerializer, UserRegisterSerializer, UserLoginSerializer
from .models import Product, User, VerificationCode
from django.db.models import Q
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import random
from django.core.mail import send_mail


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
@permission_classes([IsAuthenticated])
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
    try:
        product = Product.objects.get(productID=pk)  # Adjust field name as per your model
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    
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
@permission_classes([IsAuthenticated])
def ShowAllUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ViewUser(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def CreateUser(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=201)
    return Response(serializer.errors, status=400)

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



class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Save user to the database
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )

            # Generate and save the verification code
            verification_code = f"{random.randint(0, 9999):04}"
            VerificationCode.objects.create(email=user.email, code=verification_code)

            # Send the code to the user's email
            send_mail(
                'Your Verification Code',
                f'Your verification code is: {verification_code}',
                'your-email@example.com',  # Use a valid email here
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "User registered successfully. Please check your email for the verification code."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate or retrieve token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "message": "Login successful"
            }, status=status.HTTP_200_OK)

        return Response({"error": "Email or Password is Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyCodeView(APIView):
    def post(self, request, email):
        code = request.data.get('verification_code')

        if not code:
            return Response({"error": "Verification code is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check the verification code against the email
            verification = VerificationCode.objects.get(email=email, code=code)
        except VerificationCode.DoesNotExist:
            # If the code is invalid, delete the user and verification code
            try:
                user = User.objects.get(email=email)
                user.delete()  # Delete the user if the code is wrong
            except User.DoesNotExist:
                pass  # If the user doesn't exist, no need to delete anything
            verification.delete()  # Delete the verification code if the code is wrong
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

        # If the code is valid, keep the user and verification code
        # You can add additional actions here to activate the user if needed.

        return Response({"message": "Verification successful! User registered."}, status=status.HTTP_200_OK)

