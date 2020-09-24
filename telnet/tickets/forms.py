from django import forms
from .models import MvmImport, SielteImport
from autentication.models import User

class MvmImportForm(forms.ModelForm):

    class Meta:
        model = MvmImport
        fields = [
        'tipo_linea',
        'status',
        'ko_reason',
        'msan',
        'rete_rigida',
        'cavo_cp_cavo',
        'colonna_cp_colonna',
        'rl_cp_rl',
        'secondaria',
        'derivato',
        'presa',
        'cavetto',
        'stato_cavo',
        'note',
        'tipologia_modem',
        'seriale_modem',
        'assigned_to',
        ]

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
    status = forms.ChoiceField(widget=forms.Select, choices=(('TUTTI', 'TUTTI'), ('OK', 'OK'),('KO', 'KO'), ('SOSPESO','SOSPESO'), ('ANNULLATO','ANNULLATO')), required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    company = forms.ChoiceField(widget=forms.Select, choices=(('TUTTI', 'TUTTI'), ('MVM', 'MVM'), ('SIELTE', 'SIELTE'),), required=False)
