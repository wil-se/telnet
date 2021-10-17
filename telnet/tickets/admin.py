from django.contrib import admin
from .models import SielteImport, SielteActivity, SielteExtraActivity, UploadedFileSielte, SielteExport

admin.site.register(SielteImport)
admin.site.register(SielteActivity)
admin.site.register(SielteExtraActivity)
admin.site.register(UploadedFileSielte)
admin.site.register(SielteExport)

