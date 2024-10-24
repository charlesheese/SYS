from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . serializer import ProductSerializer
from . models import Product

from . serializer import UserSerializer
from . models import User

# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/product-list/',
        'Detail View': '/product-detail/<int:id>',
        'Create': '/product-create',
        'Update': '/product-update/<int:id>',
        'Delete': '/product-delete/<int:id>',
    }

    return Response(api_urls);

@api_view(['GET'])
def ShowAll(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def ViewProduct(request, pk):
    products = Product.objects.get(id=pk)
    serializer = ProductSerializer(products, many = False)
    return Response(serializer.data)

@api_view(['POST'])
def CreateProduct(request):
    serializer = ProductSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST'])
def UpdateProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(instance = product, data = request.data)
    if serializer.is_valid():
        serializer.save() 

    return Response(serializer.data)

@api_view(['GET'])
def DeleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()

    return Response('User Deleted sucessesfully')

@api_view(['POST'])
def UpdateUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(instance = user, data = request.data)
    if serializer.is_valid():
        serializer.save() 
