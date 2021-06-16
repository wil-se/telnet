from django.db import models
from django import forms
from django.utils import timezone

class Note(models.Model):
    note = models.TextField(max_length=2048, blank=True, null=True)
    assigned_to = models.ForeignKey('authentication.User', default=None, on_delete=models.SET_DEFAULT, blank=True, null=True, related_name='assigned_to')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('authentication.User', default=None, on_delete=models.SET_DEFAULT, blank=True, null=True, related_name='created_by')
    start_date = models.DateField(max_length=256, blank=True, null=True)
    end_date = models.DateField(max_length=256, blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.assigned_to.first_name, self.assigned_to.last_name, self.created_at)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        
