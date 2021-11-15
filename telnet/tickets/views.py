from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SielteImport, SielteActivity, SielteExtraActivity, UploadedFileSielte, SielteExport
from .forms import SielteImportForm, SearchForm
from itertools import chain
from django.db.models import Q
import datetime
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.http import HttpResponseRedirect
from authentication.models import User
import pandas as pd
from PyPDF2 import PdfFileReader, PdfFileWriter
from tika import parser
import os
import locale
import random
from django.core.paginator import Paginator
import traceback


@login_required(login_url='/accounts/login/')
def sielte_ticket(request, id):
    sielte_ticket = SielteImport.objects.get(pk=id)
    form_fields = {}
    form_fields['status'] = sielte_ticket.status
    form_fields['ko_reason'] = sielte_ticket.ko_reason
    form_fields['note'] = sielte_ticket.note
    form_fields['attivita'] = sielte_ticket.attivita
    form_fields['attivita_aggiuntiva'] = sielte_ticket.attivita_aggiuntiva
    form_fields['ora_da'] = sielte_ticket.ora_da
    form_fields['ora_a'] = sielte_ticket.ora_a
    form_fields['numero_agg'] = sielte_ticket.numero_agg
    form_fields['assigned_to'] = sielte_ticket.assigned_to

    form = SielteImportForm(request.POST or None, request.FILES or None, initial=form_fields)
    if form.is_valid():
        form.save()

    uploaded_files = UploadedFileSielte.objects.filter(obj=sielte_ticket)
    extra_price = ''
    if sielte_ticket.attivita_aggiuntiva:
        extra_price = sielte_ticket.attivita_aggiuntiva.guadagno * sielte_ticket.numero_agg

    return render(request, 'sielte_ticket.html', {'title':'Ticket Sielte', 'sielte':sielte_ticket,'form': form, 'id':id, 'uploaded_files': uploaded_files, 'extra_price': extra_price})


@login_required(login_url='/accounts/login/')
def ticket_list(request, page=1):

    if request.user.role < 3:
        text = request.GET.get('text','')
        userpk = request.GET.get('user', '')
        status = request.GET.get('status', '')
        date = request.GET.get('date', '')
        company = request.GET.get('company', '')

        sielte_queryset = Q()

        if text:
            print("TEXT: " +text)
            sielte_queryset &= (
            Q(nr__icontains=text)|
            Q(nome__icontains=text)|
            Q(indirizzo__icontains=text)
            )

        if userpk:
            user = User.objects.get(pk=userpk)
            print(user)
            sielte_queryset &= (Q(assigned_to=user))

        if status:
            print(status)
            if status != 'TUTTI':
                sielte_queryset &= (Q(status=status))

        start_date = ''
        end_date = ''

        if date:
            start_date = datetime.datetime.strptime(date.split(' - ')[0], '%d/%m/%Y')
            end_date = datetime.datetime.strptime(date.split(' - ')[1], '%d/%m/%Y')

            sielte_queryset &= (
            Q(data_inizio_appuntamento__gte=start_date)&
            Q(data_inizio_appuntamento__lte=end_date)
            )
        else:
            start_date = datetime.datetime.now()
            end_date = datetime.datetime.now()

        if company == 'TUTTI':
            tickets = list(chain([], SielteImport.objects.filter(sielte_queryset).distinct()))
        elif company == 'SIELTE':
            tickets = SielteImport.objects.filter(sielte_queryset).distinct()

        if not text and not status and not date and not company and not userpk:
            tickets = list(chain([], SielteImport.objects.filter(data_inizio_appuntamento__gte=start_date, data_inizio_appuntamento__lte=end_date)))



        paginator = Paginator(tickets, 10)

        if paginator.num_pages - page < 0 or page > paginator.num_pages or page <= 0:
            return HttpResponseRedirect('/lista-ticket')

        tickets = paginator.page(page)

        form_fields = {}
        form_fields['text'] = ''
        form_fields['status'] = ''
        form_fields['user'] = ''
        form_fields['end_date'] = ''
        form_fields['start_date'] = ''
        form_fields['company'] = ''
        form = SearchForm(request.GET or None, request.FILES or None, initial=form_fields)

        
        date = '{} - {}'.format(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))

        pages = []

        if paginator.num_pages <= 4:
            pages = [ x for x in range(1, paginator.num_pages+1)]

        else:
            left = paginator.num_pages - page
            if left > 3:
                if page <= 2:
                    pages = [ x for x in range(1, 6)]
                else:
                    pages = [ x for x in range(page-2, page+3)]
            else:
                pages = [ x for x in range(paginator.num_pages-4, page+left+1)]


        return render(request, 'ticket_list.html', {
            'title':'Lista ticket',
            'subtext': 'Tickets',
            'tickets': tickets,
            'form': form,
            'date': date,
            'start_date': start_date.strftime('%d/%m/%Y'),
            'end_date': end_date.strftime('%d/%m/%Y'),
            'pages': pages,
            'page_current': page,
            'pages_total': paginator.num_pages
            })

    else:
        text = request.GET.get('text','')
        status = request.GET.get('status', '')
        date = request.GET.get('date', '')
        company = request.GET.get('company', '')

        sielte_queryset = Q()

        if text:
            print("TEXT: " +text)
            sielte_queryset &= (
            Q(nr__icontains=text)|
            Q(nr__icontains=text)|
            Q(nome__icontains=text)|
            Q(indirizzo__icontains=text)
            )

        user = User.objects.get(pk=request.user.pk)
        sielte_queryset &= (Q(assigned_to=user))

        if status:
            print(status)
            if status != 'TUTTI':
                sielte_queryset &= (Q(status=status))

        start_date = ''
        end_date = ''

        if date:
            start_date = datetime.datetime.strptime(date.split(' - ')[0], '%d/%m/%Y')
            end_date = datetime.datetime.strptime(date.split(' - ')[1], '%d/%m/%Y')

            sielte_queryset &= (
            Q(data_inizio_appuntamento__gte=start_date)&
            Q(data_inizio_appuntamento__lte=end_date)
            )
        else:
            start_date = datetime.datetime.now()
            end_date = datetime.datetime.now()

        sielte_tickets = SielteImport.objects.filter(sielte_queryset).distinct()

        tickets = ''

        if company == 'TUTTI':
            tickets = list(chain([], sielte_tickets))
        elif company == 'SIELTE':
            tickets = SielteImport.objects.filter(sielte_queryset).distinct()

        if not text and not status and not date and not company:
            tickets = list(chain([], SielteImport.objects.filter(assigned_to=user)))


        paginator = Paginator(tickets, 10)

        if paginator.num_pages - page < 0 or page > paginator.num_pages or page <= 0:
            return HttpResponseRedirect('/lista-ticket')

        tickets = paginator.page(page)

        form_fields = {}
        form_fields['text'] = ''
        form_fields['status'] = ''
        form_fields['end_date'] = ''
        form_fields['start_date'] = ''
        form_fields['company'] = ''
        form = SearchForm(request.GET or None, request.FILES or None, initial=form_fields)

        
        date = '{} - {}'.format(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'))

        pages = []

        if paginator.num_pages <= 4:
            pages = [ x for x in range(1, paginator.num_pages+1)]

        else:
            left = paginator.num_pages - page
            if left > 3:
                if page <= 2:
                    pages = [ x for x in range(1, 6)]
                else:
                    pages = [ x for x in range(page-2, page+3)]
            else:
                pages = [ x for x in range(paginator.num_pages-4, page+left+1)]


        return render(request, 'ticket_list.html', {
            'title':'Lista ticket',
            'subtext': 'Tickets',
            'tickets': tickets,
            'form': form,
            'date': date,
            'start_date': start_date.strftime('%d/%m/%Y'),
            'end_date': end_date.strftime('%d/%m/%Y'),
            'pages': pages,
            'page_current': page,
            'pages_total': paginator.num_pages
            })


@login_required(login_url='/accounts/login/')
def save_sielte_ticket(request):
    pk = request.POST.get('id', '')

    sielte_ticket = SielteImport.objects.get(pk=pk)


    assigned_to = request.POST.get('assigned_to', '')
    if assigned_to:
        usr = User.objects.get(pk=assigned_to)
        if usr:
            sielte_ticket.assigned_to = usr
    
    stato_lavoro = request.POST.get('status','')
    if stato_lavoro:
        sielte_ticket.status = stato_lavoro

    if stato_lavoro == 'KO':
        motivo_ko = request.POST.get('motivo-ko', '')
        if motivo_ko:
            sielte_ticket.ko_reason = motivo_ko

    note = request.POST.get('note', '')
    if note:
        sielte_ticket.note = note

    attivita = request.POST.get('attivita', '')
    if attivita:
        activity = SielteActivity.objects.get(servizio=attivita)
        sielte_ticket.attivita = activity

    attivita_agg = request.POST.get('attivita_aggiuntiva', '')
    if attivita_agg:
        activity_agg = SielteExtraActivity.objects.get(servizio=attivita_agg)
        numero = request.POST.get('number', '')
        if numero:
            sielte_ticket.numero_agg = numero
        activity_agg.save()
        sielte_ticket.attivita_aggiuntiva = activity_agg



    ora_da = request.POST.get('ora_da', '')
    if ora_da:
        sielte_ticket.ora_da = ora_da

    ora_a = request.POST.get('ora_a', '')
    if ora_a:
        sielte_ticket.ora_a = ora_a


    files = request.FILES.getlist('sielte-upload')
    if files:
        for f in files:
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
            fileupload = UploadedFileSielte()
            fileupload.name = filename
            fileupload.file = File(f)
            fileupload.obj = sielte_ticket
            fileupload.save()


    sielte_ticket.save()

    return HttpResponseRedirect('/sielte-ticket/'+pk)


@login_required(login_url='/accounts/login/')
def import_page(request):
    return render(request, 'import.html', {'title':'Import', 'subtext': 'Importa file di export',})

def clean(value):
    value = value.replace('_x000D_', '').replace('\'', '').strip()
    if pd.isna(value) or value == '':
        return None
    return value

def strp_datetime(date):
    if not clean(date):
        return None
    return datetime.datetime.strptime(date, '%d-%b-%y %H:%M:%S')

def strp_datetime_sielte(value):
    try:
        dt = datetime.datetime.strptime(value, '%Y-%m-%d')
    except:
        dt = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return dt

def strp_datetime_TZ(value):
    return strp_datetime_sielte(value[:value.rfind('.')].replace('T', ' '))

def strp_date(value):
    return datetime.datetime.strptime(value, '%Y-%m-%d')

def strp_time(value):
    return datetime.datetime.strptime(value, '%H:%M:%S')


@login_required(login_url='/accounts/login/')
def upload_sielte(request):
    file = request.FILES['sielte-import']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)

    with open('media/'+filename, 'rb+') as file:
        result = parse_sielte(file)

    os.remove('media/'+filename)

    return render(request, 'import_result.html', {'title':'Import', 'result':result})


def parse_sielte(file):
    xls = pd.ExcelFile(file)
    sheet = xls.parse(0, na_filter=False, dtype='object')
    sheet = sheet.replace({pd.NaT: ''}).astype(str)
    records = sheet.to_dict(orient='records')
    result = {}
    row = 0
    message = ""
    for record in records:
        row += 1
        message = ""
        same_nr = SielteImport.objects.filter(nr=record['Nr.'])
        ok_or_ko = 0
        if len(same_nr) > 0:
            for nr in same_nr:
                if nr.status == 'DA LAVORARE':
                    nr.delete()
                    message += 'Codice {} già presente nel sistema, sovrascritto. '.format(record['Nr.'])
                else:
                    ok_or_ko += 1
        if ok_or_ko == 0:
            try:
                sielte = SielteImport()
                sielte.cod_wr_committente = record['Cod. WR Committente']
                sielte.impianto = record['Impianto']
                sielte.descrizione_centrale = record['Descrizione Centrale']
                sielte.nome = record['Nome']
                sielte.indirizzo = record['Indirizzo']
                sielte.descrizione_tipologia_pratica = record['Descrizione Tipologia Pratica']
                sielte.nome_assistente = record['Nome Assistente']
                sielte.tecnico_pratica = record['Tecnico Pratica']
                sielte.data_inizio_appuntamento = strp_datetime_sielte(record['Data Inizio/Appuntamento']) if record['Data Inizio/Appuntamento'] else None
                sielte.ora_inizio_appuntamento = strp_time(record['Ora Inizio Appuntamento']) if record['Ora Inizio Appuntamento'] else None
                sielte.descrizione_pratica = record['Descrizione Pratica']
                sielte.nr = record['Nr.']
                sielte.cod_stato = record['Cod. Stato']
                sielte.nome_stato = record['Nome Stato']
                sielte.tempo_di_esecuzione = record['Tempo di Esecuzione']
                sielte.cod_centrale = record['Cod. Centrale']
                sielte.codice_progetto = record['Codice Progetto']
                sielte.citta = record['Città']
                sielte.provincia = record['Provincia']
                sielte.data_di_ricezione = strp_datetime_TZ(record['Data di Ricezione']) if record['Data di Ricezione'] else None
                sielte.aging = record['Aging']
                # strp_datetime(record['Data Inizio/Appuntamento']) if record['Data Inizio/Appuntamento'] else None
                sielte.data_scadenza = strp_datetime_sielte(record['Data Scadenza']) if record['Data Scadenza'] else None
                sielte.data_appuntamento_a = strp_datetime_sielte(record['Data Appuntamento (Al)']) if record['Data Appuntamento (Al)'] else None
                sielte.ora_fine_appuntamento = strp_time(record['Ora Fine Appuntamento']) if record['Ora Fine Appuntamento'] else None
                sielte.inizio_lavorazione_prevista = strp_datetime_TZ(record['Inizio Lavorazione Prevista']) if record['Inizio Lavorazione Prevista'] else None
                sielte.fine_lavorazione_prevista = strp_datetime_TZ(record['Fine Lavorazione Prevista']) if record['Fine Lavorazione Prevista'] else None
                sielte.data_chiusura = strp_date(record['Data Chiusura']) if record['Data Chiusura'] else None
                sielte.ora_chiusura = strp_time(record['Ora Chiusura']) if record['Ora Chiusura'] else None
                sielte.telefono_cliente_1 = record['Telefono Cliente 1']
                sielte.telefono_cliente_2 = record['Telefono Cliente 2']
                sielte.riferimento_cliente = record['Riferimento Cliente']
                sielte.nr_occorrenze = record['Nr. Occorrenze']
                sielte.e_mail = record['E-mail']
                sielte.identificativo_cliente = record['Identificativo Cliente']
                sielte.nome_ubicazione = record['Nome Ubicazione']
                sielte.pratica_chiusa = record['Pratica Chiusa']
                sielte.pratica_interna = record['Pratica Interna']
                sielte.pratica_nuova = record['Pratica Nuova']
                sielte.tipo_cliente = record['Tipo Cliente']
                sielte.tipo_telefono_1 = record['Tipo Telefono 1']
                sielte.tipo_telefono_2 = record['Tipo Telefono 2']
                if record['Tecnico Pratica']:
                    # first_name = record['Tecnico Pratica'].split()[0]
                    # last_name = record['Tecnico Pratica'].split()[1]
                    user = ''
                    try:
                        user = User.objects.get(sieltename=record['Tecnico Pratica'])
                    except:
                        pass
                    if user:
                        sielte.assigned_to = user
                print("ASSIGNED TO: ")
                print(record['Tecnico Pratica'])
                print(sielte.assigned_to)
                sielte.status = 'DA LAVORARE'
                repeat = SielteImport.objects.filter(cod_centrale=record['Cod. Centrale'], indirizzo=record['Indirizzo'])
                sielte.occorrenze = len(repeat)+1
                for r in repeat:
                    r.occorrenze = len(repeat)+1
                    r.save()
                sielte.save()
                message += '{} caricato correttamente'.format(record['Nr.'])
                result[row] = message
            except:
                message += '{} errore nel caricamento, controlla la riga {}'.format(record['Nr.'], row)
                result[row] = message
                traceback.print_exc()
        
    return result


@login_required(login_url='/accounts/login/')
def file_sielte_delete(request, ticket, id):
    file = UploadedFileSielte.objects.get(pk=id)
    file.delete()
    return HttpResponseRedirect('/sielte-ticket/'+str(ticket))


@login_required(login_url='/accounts/login/')
def export(request):
    sielte_exports = SielteExport.objects.all()
    return render(request, 'export.html', {'title':'Export','subtext': 'Risultati export', 'sielte_exports': sielte_exports})


@login_required(login_url='/accounts/login/')
def export_sielte_delete(request, id):
    file = SielteExport.objects.get(pk=id)
    os.remove('media/sielte_export/'+file.name)
    file.delete()
    return HttpResponseRedirect('/export')


@login_required(login_url='/accounts/login/')
def export_tickets(request):
    text = request.GET.get('text','')
    userpk = request.GET.get('user', '')
    status = request.GET.get('status', '')
    date = request.GET.get('date', '')
    company = request.GET.get('company', '')
    print(company)
    sielte_queryset = Q()

    if text:
        print("TEXT: " +text)
        sielte_queryset &= (
        Q(nr__icontains=text)|
        Q(nome__icontains=text)|
        Q(indirizzo__icontains=text)
        )

    if userpk:
        user = User.objects.get(pk=userpk)
        print(user)
        sielte_queryset &= (Q(assigned_to=user))


    if status:
        print(status)
        if status != 'TUTTI':
            sielte_queryset &= (Q(status=status))

    if date:
        start_date = datetime.datetime.strptime(date.split(' - ')[0], '%m/%d/%Y')
        end_date = datetime.datetime.strptime(date.split(' - ')[1], '%m/%d/%Y')
        sielte_queryset &= (
        Q(data_inizio_appuntamento__gte=start_date)&
        Q(data_inizio_appuntamento__lte=end_date)
        )

    sielte_tickets = SielteImport.objects.filter(sielte_queryset).distinct()
    tickets = list(chain([], sielte_tickets))

    if company == 'TUTTI' or company == '':
        print('AOOO')

    if company == 'TUTTI' or company == 'SIELTE':
        sielte_assigned_to = []
        sielte_desc_tipo_pratica = []
        sielte_desc_pratica = []
        sielte_desccent = []
        sielte_wr = []
        sielte_impianto = []
        sielte_nome = []
        sielte_indirizzo = []
        sielte_data_inizio = []
        sielte_ora_inizio = []
        sielte_status = []
        sielte_compilazione = []
        sielte_guadagno = []
        sielte_aging = []
        sielte_citta = []
        sielte_cod_centrale = []
        sielte_cod_stato = []
        sielte_cod_wr_committente = []
        sielte_codice_progetto = []
        sielte_data_appuntamento_a = []
        sielte_data_chiusura = []
        sielte_data_di_ricezione = []
        sielte_data_inizio_appuntamento = []
        sielte_data_scadenza = []
        sielte_descrizione_pratica = []
        sielte_descrizione_tipologia_pratica = []
        sielte_email = []
        sielte_fine_lavorazione_prevista = []
        sielte_identificativo_cliente = []
        sielte_impianto = []
        sielte_indirizzo = []
        sielte_inizio_lavorazione_prevista = []
        sielte_nome = []
        sielte_nome_assistente = []
        sielte_nome_stato = []
        sielte_nome_ubicazione = []
        sielte_nr = []
        sielte_nr_occorrenze = []
        sielte_ora_chiusura = []
        sielte_ora_fine_appuntamento = []
        sielte_ora_inizio_appuntamento = []
        sielte_pratica_chiusa = []
        sielte_pratica_interna = []
        sielte_pratica_nuova = []
        sielte_provincia = []
        sielte_riferimento_cliente = []
        sielte_tecnico_pratica = []
        sielte_telefono_cliente_uno = []
        sielte_telefono_cliente_due = []
        sielte_tempo_di_esecuzione = []
        sielte_tipo_cliente = []
        sielte_tipo_telefono_uno = []
        sielte_tipo_telefono_due = []
        
        
        for sielte in sielte_tickets:
            sielte_assigned_to.append(sielte.assigned_to) if sielte.assigned_to else sielte_assigned_to.append('')
            sielte_desc_tipo_pratica.append(sielte.descrizione_tipologia_pratica) if sielte.descrizione_tipologia_pratica else sielte_desc_tipo_pratica.append('')
            sielte_desc_pratica.append(sielte.descrizione_pratica) if sielte.descrizione_pratica else sielte_desc_pratica.append('')
            sielte_desccent.append(sielte.descrizione_centrale) if sielte.descrizione_centrale else sielte_desccent.append('')
            sielte_wr.append(sielte.cod_wr_committente) if sielte.cod_wr_committente else sielte_nr.append('')
            sielte_impianto.append(sielte.impianto) if sielte.impianto else sielte_impianto.append('')
            sielte_nome.append(sielte.nome) if sielte.nome else sielte_nome.append('')
            sielte_indirizzo.append(sielte.indirizzo) if sielte.indirizzo else sielte_indirizzo.append('')
            sielte_data_inizio.append(sielte.data_inizio_appuntamento) if sielte.data_inizio_appuntamento else sielte_data_inizio.append('')
            sielte_ora_inizio.append(sielte.ora_inizio_appuntamento) if sielte.ora_inizio_appuntamento else sielte_ora_inizio.append('')
            sielte_status.append(sielte.status) if sielte.status else sielte_status.append('')
            
            if sielte.status == 'OK':
                sielte_guadagno.append(str(sielte.tot_price).replace('.', ',')) if sielte.tot_price else sielte_guadagno.append('')
            else:
                sielte_guadagno.append('')

            compilazione = ''
            if sielte.note:
                compilazione += 'NOTE: '+sielte.note.strip()+'\n'
            if sielte.attivita:
                compilazione += 'ATTIVITÀ: '+sielte.attivita.servizio.strip()+'\n'
            if sielte.attivita_aggiuntiva:
                compilazione += 'ATTIVITÀ AGGIUNTIVA: '+sielte.attivita_aggiuntiva.servizio.strip()+'\n'
            if sielte.ko_reason:
                compilazione += 'MOTIVO KO: '+sielte.ko_reason.strip()+'\n'
            if sielte.ora_da:
                compilazione += 'ORA DA: '+str(sielte.ora_da)+'\n'
            if sielte.ora_a:
                compilazione += 'ORA A: '+str(sielte.ora_a)+'\n'
            
            sielte_compilazione.append(compilazione)

            sielte_aging.append(sielte.aging) if sielte.aging else sielte_aging.append('')
            sielte_citta.append(sielte.citta) if sielte.citta else sielte_citta.append('')
            sielte_cod_centrale.append(sielte.cod_centrale) if sielte.cod_centrale else sielte_cod_centrale.append('')
            sielte_cod_stato.append(sielte.cod_stato) if sielte.cod_stato else sielte_cod_stato.append('')
            sielte_cod_wr_committente.append(sielte.cod_wr_committente) if sielte.cod_wr_committente else sielte_cod_wr_committente.append('')
            sielte_codice_progetto.append(sielte.codice_progetto) if sielte.codice_progetto else sielte_codice_progetto.append('')
            sielte_data_appuntamento_a.append(sielte.data_appuntamento_a) if sielte.data_appuntamento_a else sielte_data_appuntamento_a.append('')
            sielte_data_chiusura.append(sielte.data_chiusura) if sielte.data_chiusura else sielte_data_chiusura.append('')
            sielte_data_di_ricezione.append(sielte.data_di_ricezione) if sielte.data_di_ricezione else sielte_data_di_ricezione.append('')
            sielte_data_scadenza.append(sielte.data_scadenza) if sielte.data_scadenza else sielte_data_scadenza.append('')
            sielte_descrizione_pratica.append(sielte.descrizione_pratica) if sielte.descrizione_pratica else sielte_descrizione_pratica.append('')
            sielte_descrizione_tipologia_pratica.append(sielte.descrizione_tipologia_pratica) if sielte.descrizione_tipologia_pratica else sielte_descrizione_tipologia_pratica.append('')
            sielte_email.append(sielte.mail) if sielte.mail else sielte_email.append('')
            sielte_fine_lavorazione_prevista.append(sielte.fine_lavorazione_prevista) if sielte.fine_lavorazione_prevista else sielte_fine_lavorazione_prevista.append('')
            sielte_identificativo_cliente.append(sielte.identificativo_cliente) if sielte.identificativo_cliente else sielte_identificativo_cliente.append('')
            sielte_inizio_lavorazione_prevista.append(sielte.inizio_lavorazione_prevista) if sielte.inizio_lavorazione_prevista else sielte_inizio_lavorazione_prevista.append('')
            sielte_nome_assistente.append(sielte.nome_assistente) if sielte.nome_assistente else sielte_nome_assistente.append('')
            sielte_nome_stato.append(sielte.nome_stato) if sielte.nome_stato else sielte_nome_stato.append('')
            sielte_nome_ubicazione.append(sielte.nome_ubicazione) if sielte.nome_ubicazione else sielte_nome_ubicazione.append('')
            sielte_nr.append(sielte.nr) if sielte.nr else sielte_nr.append('')
            sielte_nr_occorrenze.append(sielte.nr_occorrenze) if sielte.nr_occorrenze else sielte_nr_occorrenze.append('')
            sielte_ora_chiusura.append(sielte.ora_chiusura) if sielte.ora_chiusura else sielte_ora_chiusura.append('')
            sielte_ora_fine_appuntamento.append(sielte.ora_fine_appuntamento) if sielte.ora_fine_appuntamento else sielte_ora_fine_appuntamento.append('')
            sielte_pratica_chiusa.append(sielte.pratica_chiusa) if sielte.pratica_chiusa else sielte_pratica_chiusa.append('')
            sielte_pratica_interna.append(sielte.pratica_interna) if sielte.pratica_interna else sielte_pratica_interna.append('')
            sielte_pratica_nuova.append(sielte.pratica_nuova) if sielte.pratica_nuova else sielte_pratica_nuova.append('')
            sielte_provincia.append(sielte.provincia) if sielte.provincia else sielte_provincia.append('')
            sielte_riferimento_cliente.append(sielte.riferimento_cliente) if sielte.riferimento_cliente else sielte_riferimento_cliente.append('')
            sielte_tecnico_pratica.append(sielte.tecnico_pratica) if sielte.tecnico_pratica else sielte_tecnico_pratica.append('')
            sielte_telefono_cliente_uno.append(sielte.telefono_cliente_1) if sielte.telefono_cliente_1 else sielte_telefono_cliente_uno.append('')
            sielte_telefono_cliente_due.append(sielte.telefono_cliente_2) if sielte.telefono_cliente_2 else sielte_telefono_cliente_due.append('')
            sielte_tempo_di_esecuzione.append(sielte.tempo_di_esecuzione) if sielte.tempo_di_esecuzione else sielte_tempo_di_esecuzione.append('')
            sielte_tipo_cliente.append(sielte.tipo_cliente) if sielte.tipo_cliente else sielte_tipo_cliente.append('')
            sielte_tipo_telefono_uno.append(sielte.tipo_telefono_1) if sielte.tipo_telefono_1 else sielte_tipo_telefono_uno.append('')
            sielte_tipo_telefono_due.append(sielte.tipo_telefono_2) if sielte.tipo_telefono_2 else sielte_tipo_telefono_due.append('')


        print(len(sielte_assigned_to))
        print(len(sielte_desc_tipo_pratica))
        print(len(sielte_desc_pratica))
        print(len(sielte_desccent))
        print(len(sielte_nr))
        print(len(sielte_impianto))
        print(len(sielte_nome))
        print(len(sielte_indirizzo))
        print(len(sielte_data_inizio))
        print(len(sielte_ora_inizio))
        print(len(sielte_status))
        print(len(sielte_compilazione))
        print(len(sielte_guadagno))
        print(len(sielte_aging))
        print(len(sielte_citta))
        print(len(sielte_cod_centrale))
        print(len(sielte_cod_stato))
        print(len(sielte_cod_wr_committente))
        print(len(sielte_codice_progetto))
        print(len(sielte_data_appuntamento_a))
        print(len(sielte_data_chiusura))
        print(len(sielte_data_di_ricezione))
        print(len(sielte_data_scadenza))
        print(len(sielte_descrizione_pratica))
        print(len(sielte_descrizione_tipologia_pratica))
        print(len(sielte_email))
        print(len(sielte_fine_lavorazione_prevista))
        print(len(sielte_identificativo_cliente))
        print(len(sielte_impianto))
        print(len(sielte_indirizzo))
        print(len(sielte_inizio_lavorazione_prevista))
        print(len(sielte_nome))
        print(len(sielte_nome_assistente))
        print(len(sielte_nome_stato))
        print(len(sielte_nome_ubicazione))
        print(len(sielte_nr))
        print(len(sielte_nr_occorrenze))
        print(len(sielte_data_chiusura))
        print(len(sielte_ora_chiusura))
        print(len(sielte_ora_fine_appuntamento))
        print(len(sielte_ora_inizio_appuntamento))
        print(len(sielte_pratica_chiusa))
        print(len(sielte_pratica_interna))
        print(len(sielte_pratica_nuova))
        print(len(sielte_provincia))
        print(len(sielte_riferimento_cliente))
        print(len(sielte_tecnico_pratica))
        print(len(sielte_telefono_cliente_uno))
        print(len(sielte_telefono_cliente_due))
        print(len(sielte_tempo_di_esecuzione))
        print(len(sielte_tipo_cliente))
        print(len(sielte_tipo_telefono_uno))
        print(len(sielte_tipo_telefono_due))
        print("\n\n\n\n\n\n\n\n")

        sielte_df = pd.DataFrame({
            'assegnato a': sielte_assigned_to,
            'descrizione tipo pratica': sielte_desc_tipo_pratica,
            'descrizione pratica': sielte_desc_pratica,
            'descrizione centrale': sielte_desccent,
            'nr': sielte_nr,
            'impianto': sielte_impianto,
            'nome': sielte_nome,
            'indirizzo': sielte_indirizzo,
            'data inizio': sielte_data_inizio,
            'ora inizio': sielte_ora_inizio,
            'status': sielte_status,
            'compilazione': sielte_compilazione,
            'prezzo': sielte_guadagno,
            'aging': sielte_aging,
            'citta': sielte_citta,
            'cod centrale': sielte_cod_centrale,
            'cod stato': sielte_cod_stato,
            'cod wr committente': sielte_cod_wr_committente,
            'codice progetto': sielte_codice_progetto,
            'data appuntamento al': sielte_data_appuntamento_a,
            'data chiusura': sielte_data_chiusura,
            'data di ricezione': sielte_data_di_ricezione,
            'data scadenza': sielte_data_scadenza,
            'descrizione pratica': sielte_descrizione_pratica,
            'descrizione tipologia pratica': sielte_descrizione_tipologia_pratica,
            'email': sielte_email,
            'fine lavorazione prevista': sielte_fine_lavorazione_prevista,
            'identificativo cliente': sielte_identificativo_cliente,
            'impianto': sielte_impianto,
            'inizio lavorazione prevista': sielte_inizio_lavorazione_prevista,
            'nome assistente': sielte_nome_assistente,
            'nome stato': sielte_nome_stato,
            'nome ubicazione': sielte_nome_ubicazione,
            'nr': sielte_nr,
            'nr occorrenze': sielte_nr_occorrenze,
            'data chiusura': sielte_data_chiusura,
            'ora chiusura': sielte_ora_chiusura,
            'pratica chiusa': sielte_pratica_chiusa,
            'pratica interna': sielte_pratica_interna,
            'pratica nuova': sielte_pratica_nuova,
            'provincia': sielte_provincia,
            'riferimento cliento': sielte_riferimento_cliente,
            'tecnico pratica': sielte_tecnico_pratica,
            'telefono cliente 1': sielte_telefono_cliente_uno,
            'telefono cliente 2': sielte_telefono_cliente_due,
            'tempo di esecuzione': sielte_tempo_di_esecuzione,
            'tipo cliente': sielte_tipo_cliente,
            'tipo telefono uno': sielte_tipo_telefono_uno,
            'tipo teledono due': sielte_tipo_telefono_due,
        })

        sielte_filename = 'sielte-export-{}.xlsx'.format(datetime.datetime.now())
        writer = pd.ExcelWriter('media/sielte_export/'+sielte_filename, engine='xlsxwriter')
        sielte_df.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.save()

        sielte_export = SielteExport()
        sielte_export.name = sielte_filename
        sielte_export.file = 'sielte_export/'+sielte_filename
        sielte_export.save()

    return HttpResponseRedirect('/export')