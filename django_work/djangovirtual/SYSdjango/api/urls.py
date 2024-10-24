from django.urls import path
from . import views
urlpatterns = [
    # path('', views.apiOverview, name= 'apiOverview')
    path('product-list/', views.ShowAll, name='product-list'),
    path('product-detail/<int:pk>/', views.ViewProduct, name='product-detail'),
    path('product-create/', views.CreateProduct, name='product-create'),
    path('product-update/<int:pk>/', views.UpdateProduct, name='product-update'),
    path('product-delete/<int:pk>/', views.DeleteProduct, name='product-delete'),

    path('user-list/', views.ShowAllUsers, name='user-list'),
    path('user-detail/<int:pk>/', views.ViewUser, name='user-detail'),
    path('user-create/', views.CreateUser, name='user-create'),
    path('user-update/<int:pk>/', views.UpdateUser, name='user-update'),
    path('user-delete/<int:pk>/', views.DeleteUser, name='user-delete'),

]

