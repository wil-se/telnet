from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import *

urlpatterns = [
    path('lista-ticket/<int:page>', ticket_list, name='lista ticket' ),

    path('sielte-ticket/<int:id>', sielte_ticket, name='sielte ticket'),
    path('lista-ticket', ticket_list, name='lista ticket'),
    # path('search-tickets/<int:pagecurr>', search_tickets, name='search tickets'),
    
    path('save-sielte-ticket', save_sielte_ticket, name='save sielte ticket'),
    path('file-sielte-delete/<int:ticket>/<int:id>', file_sielte_delete, name='file sielte delete'),
    path('export-tickets', export_tickets, name='export tickets'),
    path('export', export, name='export'),
    path('export-sielte-delete/<int:id>', export_sielte_delete, name='export sielte delete'),

    path('import', import_page, name='import'),
    path('upload-sielte', upload_sielte, name='upload sielte'),

    
]
