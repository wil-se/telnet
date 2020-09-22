from django import forms
from .models import Note

class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = [
        'assigned_to',
        'note',
        'created_by',
        'start_date',
        'end_date'
        ]
        widgets = {
        'start_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Seleziona data', 'type':'date'}),
        'end_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Seleziona data', 'type':'date'}),

    }
