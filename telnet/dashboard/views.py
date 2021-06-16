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
def dashboard(request):
    if request.user.role < 3:
        note_form = NoteForm(request.POST or None, request.FILES or None, initial={})

        start_date = datetime.datetime.now() - datetime.timedelta(60)
        end_date = datetime.datetime.now() + datetime.timedelta(60)
        print(start_date.strftime('%d/%m/%Y'))
        date = '{} - {}'.format(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))
        tickets = get_tickets(start_date, end_date)
        tot_mvm = str(get_guadagno_mvm(tickets['mvm'])).replace(',', '.')
        tot_sielte = str(get_guadagno_sielte(tickets['sielte'])).replace(',', '.')
        print("CIAOCIAOCIAOCIOA")
        print(tot_mvm)
        print(tot_sielte)

        mvm_earning = split_ticket_mvm(tickets['mvm'])
        sielte_earning = split_ticket_sielte(tickets['sielte'])
        # print(tickets['mvm'])
        # print(tickets['sielte'])

        mvm_data_bar = []
        sielte_data_bar = []

        total = {}
        for user in mvm_earning:
            # print(user)
            price = mvm_earning[user]
            # print(price)
            # print(mvm_earning[user])
            if user in sielte_earning.keys():
                price += sielte_earning[user]
                # print(sielte_earning[user])
            
            total[user] = price
            # print()

        for user in sielte_earning:
            price = sielte_earning[user]
            if user in total.keys():
                price += total[user]
            else:
                total[user] = price


        total = sorted(total.items(), key=lambda x: x[1], reverse=True)
        # print(total)
        names = []
        for tot in total:
            names.append('{}\n {}'.format(tot[0], str(tot[1])))

        # print('TOTALSS')
        for user in total:
            if user[0] in mvm_earning.keys():
                mvm_data_bar.append(float(mvm_earning[user[0]]))
                if user[0] in sielte_earning.keys():
                    sielte_data_bar.append(float(sielte_earning[user[0]]))
                else:
                    sielte_data_bar.append('')
            elif user[0] in sielte_earning.keys():
                sielte_data_bar.append(float(sielte_earning[user[0]]))
                mvm_data_bar.append('')

        tickets = list(chain(tickets['mvm'], tickets['sielte']))

        height = len(names)*50
        print(tot_mvm)
        print(tot_sielte)
        
        return render(request, 'dashboard_manager.html', {'title':'Dashboard', 'note_form': note_form, 'date': date,
        'tot_mvm': tot_mvm, 'tot_sielte': tot_sielte,
        'names':names, 'sielte_data_bar':sielte_data_bar, 'mvm_data_bar': mvm_data_bar, 'tickets': tickets, 'height':height})
    
    elif request.user.role == 3:
        mvm_tickets = MvmImport.objects.filter(assigned_to=request.user)
        sielte_tickets = SielteImport.objects.filter(assigned_to=request.user)
        tickets = list(chain(mvm_tickets, sielte_tickets))
        return render(request, 'dashboard_tecnico.html', {'title':'Dashboard', 'tickets':tickets})

@login_required(login_url='/accounts/login/')
def get_dashboard_data(request):
    if request.user.role < 3:

        note_form = NoteForm(request.POST or None, request.FILES or None, initial={})

        date = request.GET.get('date','')
        start_date = datetime.datetime.strptime(date.split(' - ')[0], '%d/%m/%Y')
        end_date = datetime.datetime.strptime(date.split(' - ')[1], '%d/%m/%Y')

        tickets = get_tickets(start_date, end_date)
        print("TICKET RESULT")
        print(tickets)
        print(tickets['mvm'])
        tot_mvm = str(get_guadagno_mvm(tickets['mvm'])).replace(',', '.')
        tot_sielte = str(get_guadagno_sielte(tickets['sielte'])).replace(',', '.')

        mvm_earning = split_ticket_mvm(tickets['mvm'])
        sielte_earning = split_ticket_sielte(tickets['sielte'])
        # print(tickets['mvm'])
        # print(tickets['sielte'])

        mvm_data_bar = []
        sielte_data_bar = []

        total = {}
        for user in mvm_earning:
            # print(user)
            price = mvm_earning[user]
            # print(price)
            # print(mvm_earning[user])
            if user in sielte_earning.keys():
                price += sielte_earning[user]
                # print(sielte_earning[user])
            
            total[user] = price
            # print()

        for user in sielte_earning:
            price = sielte_earning[user]
            if user in total.keys():
                price += total[user]
            else:
                total[user] = price


        total = sorted(total.items(), key=lambda x: x[1], reverse=True)
        # print(total)
        names = []
        for tot in total:
            names.append('{}\n {}'.format(tot[0], str(tot[1])))

        # print('TOTALSS')
        for user in total:
            if user[0] in mvm_earning.keys():
                mvm_data_bar.append(float(mvm_earning[user[0]]))
                if user[0] in sielte_earning.keys():
                    sielte_data_bar.append(float(sielte_earning[user[0]]))
                else:
                    sielte_data_bar.append('')
            elif user[0] in sielte_earning.keys():
                sielte_data_bar.append(float(sielte_earning[user[0]]))
                mvm_data_bar.append('')

        tickets = list(chain(tickets['mvm'], tickets['sielte']))
        height = len(names)*50

        return render(request, 'dashboard_manager.html', {'title':'Dashboard', 'note_form': note_form, 'date': date,
        'tot_mvm': tot_mvm, 'tot_sielte': tot_sielte,
        'names':names, 'sielte_data_bar':sielte_data_bar, 'mvm_data_bar': mvm_data_bar, 'tickets': tickets, 'height': height})


def get_tickets(start_date, end_date):
    mvm_queryset = (
    Q(datainiz__gte=start_date)&
    Q(datainiz__lte=end_date)&
    Q(status='OK')
    )
    mvm_tickets = MvmImport.objects.filter(mvm_queryset).distinct()

    sielte_queryset = (
    Q(inizio_lavorazione_prevista__gte=start_date)&
    Q(inizio_lavorazione_prevista__lte=end_date)&
    Q(status='OK')
    )
    sielte_tickets = SielteImport.objects.filter(sielte_queryset).distinct()

    return {
        'mvm': mvm_tickets,
        'sielte': sielte_tickets,
    }


def get_guadagno_mvm(tickets):
    guadagno_mvm = 0

    for mvmt in tickets:
        
        if mvmt.price:
            print(mvmt.price)
            guadagno_mvm += mvmt.price
    print(guadagno_mvm)
    return guadagno_mvm

def get_guadagno_sielte(tickets):
    guadagno_sielte = 0
    print("SONO DENTRO GUADAGNO SIELTE")
    print(tickets)
    for slt in tickets:
        if slt.attivita:
            guadagno_sielte += slt.attivita.guadagno
            guadagno_sielte += slt.attivita_aggiuntiva.guadagno * slt.numero_agg
    return guadagno_sielte


def split_ticket_mvm(tickets):
    users = {}
    for ticket in tickets:
        if ticket.assigned_to not in users.keys():
            users[ticket.assigned_to] = [ticket]
        else:
            tkts = users[ticket.assigned_to]
            tkts.append(ticket)
            users[ticket.assigned_to] = tkts
    # pp.pprint(users)
    earning = {}
    for user in users:
        earning[user.email] = get_guadagno_mvm(users[user])

    return earning


def split_ticket_sielte(tickets):
    users = {}
    for ticket in tickets:
        if ticket.assigned_to not in users.keys():
            users[ticket.assigned_to] = [ticket]
        else:
            tkts = users[ticket.assigned_to]
            tkts.append(ticket)
            users[ticket.assigned_to] = tkts
    # pp.pprint(users)
    earning = {}
    for user in users:
        earning[user.email] = get_guadagno_sielte(users[user])

    return earning

def add_user(request):
    if (request.user.role < 3):
        return render(request, 'adduser.html', {})

def save_user(request):
    if (request.user.role < 3):
        username = request.POST.get('username', '')
        name = request.POST.get('name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password', '')
        password_two = request.POST.get('password_two', '')
        email = request.POST.get('email', '')
        email_two = request.POST.get('email_two', '')
        role = request.POST.get('role', '')

        print(name)
        print(last_name)
        print(password)
        print(password_two)
        print(email)
        print(email_two)
        print(role)
        
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
        if role == "Backoffide":
            newuser.role = 2
        if role == "Tecnico":
            newuser.role = 3

        newuser.save()


        return JsonResponse({'success': True})
