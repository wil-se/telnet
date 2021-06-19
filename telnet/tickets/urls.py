from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import ticket_list, save_mvm_ticket

urlpatterns = [
    path('lista-ticket/<int:page>', ticket_list, name='lista ticket' ),
    path('save-mvm-ticket', save_mvm_ticket, name='save mvm ticket'),
]
