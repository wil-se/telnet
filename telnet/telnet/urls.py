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
from notes.urls import urlpatterns as notes


urlpatterns = [
    path('', lambda req: redirect('/dashboard')),

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', include('dashboard.urls')),
    path('', include('authentication.urls')),
    path('', include('tickets.urls')),
    path('', include('notes.urls')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
