from django.contrib import admin
from django.urls import path, include
from .views import Home, register, Dashboard, AddItem, EditItem, DeleteItem
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', Home.as_view(), name='home'),
    path('register',register, name='register'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    
]