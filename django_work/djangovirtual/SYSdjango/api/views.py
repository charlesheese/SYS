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
        # Validate the incoming data
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Temporarily store user data in the session (do not save to the database yet)
            request.session['user_data'] = serializer.validated_data

            # Generate a random verification code
            verification_code = f"{random.randint(0, 9999):04}"  # Zero-padded 4-digit string

            # Save the verification code in the database
            VerificationCode.objects.create(email=serializer.validated_data['email'], code=verification_code)

            # Send the verification code to the user's email
            send_mail(
                'Your Verification Code',
                f'Your verification code is: {verification_code}',
                'abhaywade05@gmail.com',
                [serializer.validated_data['email']],
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
        # The email is obtained from the URL, so we only validate the code
        code = request.data.get('verification_code')

        if not code:
            return Response(
                {"error": "Verification code is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 1: Check if the verification code matches the email
        try:
            verification = VerificationCode.objects.get(email=email, code=code)
        except VerificationCode.DoesNotExist:
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Retrieve user data from the session
        user_data = request.session.get('user_data')

        if not user_data or user_data['email'] != email:
            return Response({"error": "No user data found or email mismatch."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Create and save the user to the database
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']  # Hashing handled by `create_user`
        )

        # Step 4: Delete the verification code after successful verification
        verification.delete()

        # Step 5: Clear session data after saving the user
        request.session.pop('user_data', None)

        return Response(
            {"message": "Verification successful! User registered."},
            status=status.HTTP_200_OK
        )






