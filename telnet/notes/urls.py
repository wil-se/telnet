from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import *

urlpatterns = [
    path('lista-note', note_list, name='lista note'),
    path('save-note', save_note, name='save note'),
    path('nota/<int:id>', note, name='note'),
    path('modifica-nota/<int:id>', note_edit, name='note edit'),
    path('save-mod-note', save_mod_note, name='save mod note'),
    path('delete-note', delete_note, name='delete note'),
    path('search-notes', search_notes, name='search notes'),
    
]
