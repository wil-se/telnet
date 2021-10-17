from django.core.management.base import BaseCommand, CommandError
from tickets.models import SielteImport, SielteActivity
import random
from authentication.models import User
from datetime import datetime

class Command(BaseCommand):

    def add_arguments(self, parser):
        #parser.add_argument('path', type=str, help='randomize database')
        pass
    
    def handle(self, *args, **options):
        sielte_q = SielteImport.objects.all()

        for sielte in sielte_q:
            sielte.status = random.choice(["OK", "KO", "SOSPESO", "ANNULLATO", "DA LAVORARE"])
            emails = list(User.objects.all().values_list('email'))
            sielte.assigned_to = User.objects.get(email=random.choice(emails)[0])
            sielte.attivita = SielteActivity.objects.get(servizio="ADSL A + router")
            sielte.data_inizio_appuntamento = datetime.now()
            
            sielte.save()
    