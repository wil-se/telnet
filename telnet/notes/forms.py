from django import forms
from .models import Note
from datetime import datetime

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

