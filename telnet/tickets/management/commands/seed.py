from django.core.management.base import BaseCommand, CommandError
from tickets.models import MvmImport, SielteImport
import random
from authentication.models import User

class Command(BaseCommand):

    def add_arguments(self, parser):
        #parser.add_argument('path', type=str, help='randomize database')
        pass
    
    def handle(self, *args, **options):
        mvm_q = MvmImport.objects.all()
        sielte_q = SielteImport.objects.all()

        for mvm in mvm_q:
            mvm.status = random.choice(["OK", "KO", "SOSPESO", "ANNULLATO"])
            emails = list(User.objects.all().values_list('email'))
            mvm.assigned_to = User.objects.get(email=random.choice(emails)[0])
            mvm.save()
        

        for sielte in sielte_q:
            sielte.status = random.choice(["OK", "KO", "SOSPESO", "ANNULLATO"])
            emails = list(User.objects.all().values_list('email'))
            sielte.assigned_to = User.objects.get(email=random.choice(emails)[0])
            sielte.save()
    