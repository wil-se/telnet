from django.contrib import admin
from django.urls import path, include
from dashboard import views as dashboard_views
from tickets import views as tickets_views
from notes import views as notes_views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from dashboard.urls import urlpatterns as dashboard_urls
from authentication.urls import urlpatterns as authentication_urls
from tickets.urls import urlpatterns as tickets_urls



urlpatterns = [
    path('', lambda req: redirect('/dashboard')),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('import', tickets_views    .import_page, name='import'),
    path('upload-mvm', tickets_views.upload_mvm, name='upload mvm'),
    path('upload-sielte', tickets_views.upload_sielte, name='upload sielte'),
    path('upload-mvm-pdf', tickets_views.upload_mvm_pdf, name='upload mvm pdf'),

    path('lista-note', notes_views.note_list, name='lista note'),
    path('save-note', notes_views.save_note, name='save note'),
    path('nota/<int:id>', notes_views.note, name='note'),
    path('modifica-nota/<int:id>', notes_views.note_edit, name='note edit'),
    path('save-mod-note', notes_views.save_mod_note, name='save mod note'),
    path('delete-note', notes_views.delete_note, name='delete note'),
    path('search-notes', notes_views.search_notes, name='search notes'),

    path('', include('dashboard.urls')),
    path('', include('authentication.urls')),
    path('', include('tickets.urls')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
