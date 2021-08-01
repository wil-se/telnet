from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notes.forms import NoteForm
import datetime
from tickets.models import MvmImport, SielteImport 
from django.db.models import Q
from itertools import chain
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from authentication.models import User



@login_required(login_url='/accounts/login/')
def dash(request):

    if request.GET.get('date',''):
        date = request.GET.get('date','')
        start_date = datetime.datetime.strptime(date.split(' - ')[0], '%d/%m/%Y')
        end_date = datetime.datetime.strptime(date.split(' - ')[1], '%d/%m/%Y')
    else:
        start_date = datetime.datetime.now() - datetime.timedelta(30)
        end_date = datetime.datetime.now() + datetime.timedelta(30)

    
    if request.user.role < 3:

        mvm_queryset = (
        Q(datainiz__gte=start_date)&
        Q(datainiz__lte=end_date)
        )
        mvm_tickets = MvmImport.objects.filter(mvm_queryset).distinct()

        sielte_queryset = (
        Q(inizio_lavorazione_prevista__gte=start_date)&
        Q(inizio_lavorazione_prevista__lte=end_date)
        )
        sielte_tickets = SielteImport.objects.filter(sielte_queryset).distinct()

        tickets = list(chain(mvm_tickets, sielte_tickets))

        ok = 0
        ko = 0
        sospesi = 0
        annullati = 0

        for ticket in tickets:
            if ticket.status == 'OK':
                ok +=1
            if ticket.status == 'KO':
                ko +=1
            if ticket.status == 'SOSPESO':
                sospesi +=1
            if ticket.status == 'ANNULLATO':
                annullati +=1


        users = User.objects.all()

        xaxis_names = []
        series_mvm = []
        series_sielte = []
        series_total = []

        for i, user in enumerate(users):
            xaxis_names.append("{}\n {}".format(user.first_name, user.last_name))
            mvm_queryset = (
            Q(datainiz__gte=start_date)&
            Q(datainiz__lte=end_date)&
            Q(status='OK')&
            Q(assigned_to=user)
            )

            sielte_queryset = (
            Q(inizio_lavorazione_prevista__gte=start_date)&
            Q(inizio_lavorazione_prevista__lte=end_date)&
            Q(status='OK')&
            Q(assigned_to=user)
            )
            series_mvm.append(int(get_guadagno_mvm(MvmImport.objects.filter(mvm_queryset).distinct())))
            series_sielte.append(int(get_guadagno_sielte(SielteImport.objects.filter(sielte_queryset).distinct())))
            series_total.append(int(series_mvm[i] + series_sielte[i]))

        return render(request, 'dash_manager.html', {
            'title':'Dashboard', 
            'subtext': 'Panoramica',
            'start_date': start_date.strftime('%d/%m/%Y'),
            'end_date': end_date.strftime('%d/%m/%Y'),
            'tot_mvm': get_guadagno_mvm(mvm_tickets),
            'tot_sielte': get_guadagno_sielte(sielte_tickets),
            'note_form': NoteForm(request.POST or None, request.FILES or None, initial={}),
            'tickets': tickets,
            'ok': ok,
            'ko': ko,
            'sospesi': sospesi,
            'annullati': annullati,
            'names': xaxis_names,
            'series_mvm': series_mvm,
            'series_sielte': series_sielte,
            'series_total': series_total,
            'bars_width': len(users)*175
            })

    else:
        mvm_queryset = (
        Q(datainiz__gte=start_date)&
        Q(datainiz__lte=end_date)&
        Q(assigned_to__pk=request.user.pk)
        )
        mvm_tickets = MvmImport.objects.filter(mvm_queryset).distinct()

        sielte_queryset = (
        Q(inizio_lavorazione_prevista__gte=start_date)&
        Q(inizio_lavorazione_prevista__lte=end_date)&
        Q(assigned_to__pk=request.user.pk)
        )
        sielte_tickets = SielteImport.objects.filter(sielte_queryset).distinct()

        tickets = list(chain(mvm_tickets, sielte_tickets))

        ok = 0
        ko = 0
        sospesi = 0
        annullati = 0

        for ticket in tickets:
            if ticket.status == 'OK':
                ok +=1
            if ticket.status == 'KO':
                ko +=1
            if ticket.status == 'SOSPESO':
                sospesi +=1
            if ticket.status == 'ANNULLATO':
                annullati +=1
        
        return render(request, 'dash_tecnico.html', {
                'title':'Dashboard', 
                'subtext': 'Panoramica',
                'start_date': start_date.strftime('%d/%m/%Y'),
                'end_date': end_date.strftime('%d/%m/%Y'),
                'tickets': tickets,
                'ok': ok,
                'ko': ko,
                'sospesi': sospesi,
                'annullati': annullati,
                })



def get_guadagno_mvm(tickets):
    guadagno_mvm = 0
    for mvmt in tickets:
        if mvmt.price:
            guadagno_mvm += mvmt.price
    return guadagno_mvm

def get_guadagno_sielte(tickets):
    guadagno_sielte = 0
    for slt in tickets:
        if slt.attivita:
            if slt.attivita.guadagno:
                guadagno_sielte += slt.attivita.guadagno
            if slt.attivita_aggiuntiva and slt.attivita_aggiuntiva.guadagno:
                guadagno_sielte += slt.attivita_aggiuntiva.guadagno * slt.numero_agg
    return guadagno_sielte


def add_user(request):
    if (request.user.role < 2):
        return render(request, 'adduser.html', {'title': 'Aggiungi utente', 'subtext': 'Gestione account',})

def save_user(request):
    if (request.user.role < 2):
        username = request.POST.get('username', '')
        name = request.POST.get('name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password', '')
        password_two = request.POST.get('password_two', '')
        email = request.POST.get('email', '')
        email_two = request.POST.get('email_two', '')
        role = request.POST.get('role', '')
        sieltename = request.POST.get('sieltename', '')
        
        
        if not username or not name or not last_name or not password_two or not password_two or not email or not email_two:
            print("check 0")
            return JsonResponse({'success': False, 'message': "Sono richiesti tutti i campi"})    


        # controlla password uguali
        if password != password_two:
            print("check 1")
            return JsonResponse({'success': False, 'message': "Le password non coincidono"})    

        # controlla email uguali
        if email != email_two:
            print("check 2")
            return JsonResponse({'success': False, 'message': "Le email non coincidono"})    
            
        # controlla email già esistente
        if User.objects.filter(email=email).exists():
            print("email già presente")
            return JsonResponse({'success': False, 'message': "Email già presente"})    
        

        newuser = User.objects.create_user(username, email, password)
        newuser.first_name = name
        newuser.last_name = last_name

        if role == "Admin":
            newuser.role = 0
        if role == "Manager":
            newuser.role = 1
        if role == "Backoffice":
            newuser.role = 2
        if role == "Tecnico":
            newuser.role = 3

        newuser.save()


        return JsonResponse({'success': True})

