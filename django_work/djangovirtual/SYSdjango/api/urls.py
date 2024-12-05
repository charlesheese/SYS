from django.urls import path
from .views import apiOverview, ShowAll, ViewProduct, CreateProduct, UpdateProduct, DeleteProduct
from .views import ShowAllUsers, ViewUser, CreateUser, UpdateUser, DeleteUser
from .views import UserRegisterView, UserLoginView


urlpatterns = [
    path('', apiOverview, name="api-overview"),
    path('product-list/', ShowAll, name="product-list"),
    path('product-detail/<int:pk>/', ViewProduct, name="product-detail"),
    path('product-create/', CreateProduct, name="product-create"),
    path('product-update/<int:pk>/', UpdateProduct, name="product-update"),
    path('product-delete/<int:pk>/', DeleteProduct, name="product-delete"),
    path('user-list/', ShowAllUsers, name="user-list"),
    path('user-detail/<int:pk>/', ViewUser, name="user-detail"),
    path('user-create/', CreateUser, name="user-create"),
    path('user-update/<int:pk>/', UpdateUser, name="user-update"),
    path('user-delete/<int:pk>/', DeleteUser, name="user-delete"),
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
]

# /api/product-list/?is_sold=false
# Sort by price ascending: /api/product-list/?sort_by=price&order=asc
# Sort by price descending: /api/product-list/?sort_by=price&order=desc
# Sort by creation date descending: /api/product-list/?sort_by=createdAtProduct&order=desc

