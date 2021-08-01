from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role_choices = (
      (0, 'admin'),
      (1, 'manager'),
      (2, 'backoffice'),
      (3, 'tecnico'),
    )

    role = models.PositiveSmallIntegerField(choices=role_choices, default=3)
    matricola = models.CharField(max_length=32, blank=True, null=True)
    residenza = models.CharField(max_length=32, blank=True, null=True)
    sieltename = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.email

    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'
