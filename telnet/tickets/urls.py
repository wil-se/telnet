from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import ticket_list

urlpatterns = [
    path('lista-ticket/<int:page>', ticket_list, name='lista_ticket' ),
]
