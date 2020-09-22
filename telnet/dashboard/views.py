from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from notes.forms import NoteForm
import datetime
from tickets.models import MvmImport, SielteImport 
from django.db.models import Q
from itertools import chain


@login_required(login_url='/accounts/login/')
def dashboard(request):
    if request.user.role < 3:
        note_form = NoteForm(request.POST or None, request.FILES or None, initial={})

        start_date = datetime.datetime.now() - datetime.timedelta(60)
        end_date = datetime.datetime.now() + datetime.timedelta(60)
        date = '{} - {}'.format(start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y'))
        tickets = get_tickets(start_date, end_date)
        tot_mvm = str(get_guadagno_mvm(tickets['mvm'])).replace(',', '.')
        tot_sielte = str(get_guadagno_sielte(tickets['sielte'])).replace(',', '.')


        mvm_earning = split_ticket_mvm(tickets['mvm'])
        sielte_earning = split_ticket_sielte(tickets['sielte'])
        print(mvm_earning)
        print()
        print(sielte_earning)
        mvm_data_bar = []
        sielte_data_bar = []

        total = {}
        for user in mvm_earning:
            # print(user)
            price = mvm_earning[user]
            print(price)
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
        print(total)
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
        print(names)
        for t in tickets:
            print('{} {}'.format(t.assigned_to.first_name, t.assigned_to.last_name))

        return render(request, 'dashboard_manager.html', {'title':'Dashboard', 'note_form': note_form, 'date': date,
        'tot_mvm': tot_mvm, 'tot_sielte': tot_sielte,
        'names':names, 'sielte_data_bar':sielte_data_bar, 'mvm_data_bar': mvm_data_bar, 'tickets': tickets,})



@login_required(login_url='/accounts/login/')
def get_dashboard_data(request):
    return render(request, 'dashboard_manager.html', {'title':'Dashboard'})



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
            guadagno_mvm += mvmt.price
    return guadagno_mvm

def get_guadagno_sielte(tickets):
    guadagno_sielte = 0
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
        earning[user.first_name+' '+user.last_name] = get_guadagno_mvm(users[user])

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
        earning[user.first_name+' '+user.last_name] = get_guadagno_sielte(users[user])

    return earning
