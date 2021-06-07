from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from tickets.models import MvmImport
import datetime
from authentication.models import User


# crea utenti a partire da un file excel (static/mansioni-prezzi.xlsx)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='mvm xlsx export file path')

    def handle(self, *args, **options):
        path = options['path']
        xls = pd.ExcelFile(path)
        sheet = xls.parse(0, na_filter=False, dtype='object')
        records = sheet.to_dict(orient='records')

        for record in records:
            user = User()
            user.username = record['MATRICOLA LUL']
            user.matricola = record['MATRICOLA LUL']
            user.first_name = record['NOME'].lower().capitalize()
            user.last_name = record['COGNOME'].lower().capitalize()
            user.email = record['MAIL']
            user.password = 'satana'
            user.is_staff = True
            user.is_active = True
            user.residenza = record['RESIDENZA']

            if record['MANSIONE'] == 'Admin':
                user.role = 0
            if record['MANSIONE'] == 'Manager':
                user.role = 1
            if record['MANSIONE'] == 'Back-office':
                user.role = 2
            if record['MANSIONE'] == 'TECNICO':
                user.role = 3

            user.save()
