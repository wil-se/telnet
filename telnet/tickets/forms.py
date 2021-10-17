from django import forms
from .models import SielteImport
from authentication.models import User


class SielteImportForm(forms.ModelForm):

    class Meta:
        model = SielteImport
        fields = [
        'status',
        'ko_reason',
        'note',
        'attivita',
        'attivita_aggiuntiva',
        'ora_da',
        'ora_a',
        'numero_agg',
        'assigned_to',
        ]

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class SearchForm(forms.Form):
    text = forms.CharField(label='Cerca', max_length=100, required=False)
    status = forms.ChoiceField(widget=forms.Select, choices=(('TUTTI', 'TUTTI'), ('OK', 'OK'),('KO', 'KO'), ('SOSPESO','SOSPESO'), ('ANNULLATO','ANNULLATO'), ('DA LAVORARE','DA LAVORARE')), required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    company = forms.ChoiceField(widget=forms.Select, choices=(('TUTTI', 'TUTTI'), ('SIELTE', 'SIELTE'),), required=False)
