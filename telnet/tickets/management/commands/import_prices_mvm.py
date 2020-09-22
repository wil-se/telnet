from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from tickets.models import MvmJob, MvmPrice
import datetime
from autentication.models import User


# date una città e un codice lavoro esiste un prezzo associato
# queste informazioni sono presenti in una tabella excel
# e vengono usate durante l'import di mvm

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='import Mvm prices from file')

    def handle(self, *args, **options):
        path = options['path']
        xls = pd.ExcelFile(path)
        sheet = xls.parse(0, na_filter=False, dtype='object').replace(0, None)
        records = sheet.to_dict(orient='records')
        data = {}
        current = ''

        for record in records:
            if record['x.1'] == '':
                data[record['x']] = {}
                current = record['x']
            else:
                city = record['x']
                price = round(record['x.1'], 2)
                d = data[current]
                d[city] = price
                data[current] = d

        for job in data.keys():
            for entry in data[job].keys():
                mvm_price = MvmPrice()

                jobtype, created = MvmJob.objects.get_or_create(
                    job_type=job,
                )

                mvm_price.job_type = jobtype
                mvm_price.desccent = str(entry)
                mvm_price.price = str(data[job][entry])
                mvm_price.save()
