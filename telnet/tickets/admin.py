from django.contrib import admin
from .models import SielteImport, SielteActivity, SielteExtraActivity, UploadedFileSielte, SielteExport


class SielteImportAdmin(admin.ModelAdmin):
    search_fields = [
        'cod_wr_committente',
        'nr',
        'impianto',
        'descrizione_centrale',
        'nome',
        'indirizzo',
    ]

admin.site.register(SielteImport, SielteImportAdmin)
admin.site.register(SielteActivity)
admin.site.register(SielteExtraActivity)
admin.site.register(UploadedFileSielte)
admin.site.register(SielteExport)

