from django.urls import path
from . import views
urlpatterns = [
    # path('', views.apiOverview, name= 'apiOverview')
    path('product-list/', views.ShowAll, name='product-list'),
    path('product-detail/<int:pk>/', views.ViewProduct, name='product-detail'),
    path('product-create/', views.CreateProduct, name='product-create'),
    path('product-update/<int:pk>/', views.UpdateProduct, name='product-update'),
    path('product-delete/<int:pk>/', views.DeleteProduct, name='product-delete'),

    path('product-list/', views.ShowAll, name='product-list'),
    path('product-detail/<int:pk>/', views.ViewProduct, name='product-detail'),
    path('product-create/', views.CreateProduct, name='product-create'),
    path('product-update/<int:pk>/', views.UpdateProduct, name='product-update'),
    path('product-delete/<int:pk>/', views.DeleteProduct, name='product-delete'),

]

