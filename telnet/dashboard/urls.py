from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import add_user, save_user, dash

urlpatterns = [
    path('add_user/', add_user, name='add user' ),
    path('save_user/', save_user, name='save user' ),
    path('dashboard/', dash, name='dashboard' ),
]
