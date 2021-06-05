from django.contrib import admin
from django.urls import path, include
from dashboard import views as dashboard_views
from tickets import views as tickets_views
from notes import views as notes_views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda req: redirect('/dashboard')),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard', dashboard_views.dashboard, name='dashboard'),
    path('get-dashboard-data', dashboard_views.get_dashboard_data, name='get dashboard data'),

    path('mvm-ticket/<int:id>', tickets_views.mvm_ticket, name='mvm ticket'),
    path('sielte-ticket/<int:id>', tickets_views.sielte_ticket, name='sielte ticket'),
    path('lista-ticket', tickets_views.ticket_list, name='lista ticket'),
    path('search-tickets', tickets_views.search_tickets, name='search tickets'),
    path('save-mvm-ticket', tickets_views.save_mvm_ticket, name='save mvm ticket'),
    path('save-sielte-ticket', tickets_views.save_sielte_ticket, name='save sielte ticket'),
    path('file-mvm-delete/<int:ticket>/<int:id>', tickets_views.file_mvm_delete, name='file mvm delete'),
    path('file-sielte-delete/<int:ticket>/<int:id>', tickets_views.file_sielte_delete, name='file sielte delete'),
    path('export-tickets', tickets_views.export_tickets, name='export tickets'),
    path('export', tickets_views.export, name='export'),
    path('export-mvm-delete/<int:id>', tickets_views.export_mvm_delete, name='export mvm delete'),
    path('export-sielte-delete/<int:id>', tickets_views.export_sielte_delete, name='export sielte delete'),

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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
