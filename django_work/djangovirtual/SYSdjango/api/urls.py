from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='apiOverview'),
    
    # Product endpoints
    path('product-list/', views.ShowAll, name='product-list'),  # Product listing with filtering support
    path('product-detail/<int:pk>/', views.ViewProduct, name='product-detail'),
    path('product-create/', views.CreateProduct, name='product-create'),
    path('product-update/<int:pk>/', views.UpdateProduct, name='product-update'),
    path('product-delete/<int:pk>/', views.DeleteProduct, name='product-delete'),
    
    # User endpoints
    path('user-list/', views.ShowAllUsers, name='user-list'),
    path('user-detail/<int:pk>/', views.ViewUser, name='user-detail'),
    path('user-create/', views.CreateUser, name='user-create'),
    path('user-update/<int:pk>/', views.UpdateUser, name='user-update'),
    path('user-delete/<int:pk>/', views.DeleteUser, name='user-delete'),
    
    # Message endpoints (if applicable)
    path('message-list/<int:sender_id>/<int:recipient_id>/', views.ShowMessagesBetweenUsers, name='message-list'),
    path('message-create/', views.CreateMessage, name='message-create'),
]
# /api/product-list/?is_sold=false
# Sort by price ascending: /api/product-list/?sort_by=price&order=asc
# Sort by price descending: /api/product-list/?sort_by=price&order=desc
# Sort by creation date descending: /api/product-list/?sort_by=createdAtProduct&order=desc

