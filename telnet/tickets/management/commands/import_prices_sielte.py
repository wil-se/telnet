from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from tickets.models import SielteExtraActivity, SielteActivity
from authentication.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='import Mvm prices from file')

    def handle(self, *args, **options):
        path = options['path']
        xls = pd.ExcelFile(path)
        sheet = xls.parse(0, na_filter=False, dtype='object').replace(0, None)
        records = sheet.to_dict(orient='records')
        print("PRICES SIELTE")
        for record in records:
            # print(record)
            attivita = str(record['ATTIVITA\''])
            
            guadagno_att = str(record['GUADAGNO']).replace('€', '').replace('-', '').strip()
            attivita_agg = str(record['ATTIVITA\' AGGIUNTIVE'])
            guadagno_agg = str(record['GUADAGNO.1']).replace('€', '').replace('-', '').strip()

            if not guadagno_att:
                guadagno_att = 0
            if not guadagno_agg:
                guadagno_agg = 0

            if attivita:
                # print('ATTIVITA: '+attivita)
                # print('GUADAGNO ATT: '+guadagno_att)
                sielte_act = SielteActivity()
                sielte_act.servizio = attivita
                sielte_act.guadagno = guadagno_att
                #print(sielte_act)
                sielte_act.save()


            if attivita_agg and guadagno_agg:
                # print('ATTIVITA AGG: '+attivita_agg)
                # print('GUADAGNO AGG: '+guadagno_agg)
                sielte_extra = SielteExtraActivity()
                sielte_extra.servizio = ''.join(i for i in attivita_agg if not i.isdigit()).strip()
                sielte_extra.guadagno = guadagno_agg
                sielte_extra.numero = 1
                try:
                    sielte_extra.save()
                except:
                    print('obj already exists')

        print("END SIELTE PRICES")
