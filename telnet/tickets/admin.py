from django.contrib import admin
from .models import MvmImport, SielteImport, MvmJob, MvmPrice, SielteActivity, SielteExtraActivity, UploadedFileMvm, UploadedFileSielte, MvmExport, SielteExport

admin.site.register(MvmImport)
admin.site.register(SielteImport)
admin.site.register(MvmJob)
admin.site.register(MvmPrice)
admin.site.register(SielteActivity)
admin.site.register(SielteExtraActivity)
admin.site.register(UploadedFileMvm)
admin.site.register(UploadedFileSielte)
admin.site.register(MvmExport)
admin.site.register(SielteExport)

