from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import *

urlpatterns = [
    path('lista-ticket/<int:page>', ticket_list, name='lista ticket' ),
    path('save-mvm-ticket', save_mvm_ticket, name='save mvm ticket'),

    path('mvm-ticket/<int:id>', mvm_ticket, name='mvm ticket'),
    path('sielte-ticket/<int:id>', sielte_ticket, name='sielte ticket'),
    path('lista-ticket', ticket_list, name='lista ticket'),
    # path('search-tickets/<int:pagecurr>', search_tickets, name='search tickets'),
    
    path('save-sielte-ticket', save_sielte_ticket, name='save sielte ticket'),
    path('file-mvm-delete/<int:ticket>/<int:id>', file_mvm_delete, name='file mvm delete'),
    path('file-sielte-delete/<int:ticket>/<int:id>', file_sielte_delete, name='file sielte delete'),
    path('export-tickets', export_tickets, name='export tickets'),
    path('export', export, name='export'),
    path('export-mvm-delete/<int:id>', export_mvm_delete, name='export mvm delete'),
    path('export-sielte-delete/<int:id>', export_sielte_delete, name='export sielte delete'),

]
