from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import logout_view

urlpatterns = [
    path('logout/', logout_view, name='logout' ),
    
]
