from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MvmImport, SielteImport, SielteActivity, SielteExtraActivity, UploadedFileMvm, UploadedFileSielte, MvmPrice, MvmJob
from .forms import MvmImportForm, SielteImportForm, SearchForm
from itertools import chain
from django.db.models import Q
import datetime
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.http import HttpResponseRedirect
from autentication.models import User
import pandas as pd
from PyPDF2 import PdfFileReader, PdfFileWriter
from tika import parser
import os
import locale


@login_required(login_url='/accounts/login/')
def mvm_ticket(request, id):
    mvm_ticket = MvmImport.objects.get(pk=id)
    form_fields={}
    form_fields['tipo_linea'] = mvm_ticket.tipo_linea
    form_fields['status'] = mvm_ticket.status
    form_fields['secondaria'] = mvm_ticket.secondaria
    form_fields['derivato'] = mvm_ticket.derivato
    form_fields['presa'] = mvm_ticket.presa
    form_fields['cavetto'] = mvm_ticket.cavetto
    form_fields['note'] = mvm_ticket.note
    form_fields['tipologia_modem'] = mvm_ticket.tipologia_modem
    form_fields['seriale_modem'] = mvm_ticket.seriale_modem
    form_fields['assigned_to'] = mvm_ticket.assigned_to
    form = MvmImportForm(request.POST or None, request.FILES or None, initial=form_fields)
    if form.is_valid():
        form.save()
    
    uploaded_files = UploadedFileMvm.objects.filter(obj=mvm_ticket)

    return render(request, 'mvm_ticket.html', {'title':'', 'mvm':mvm_ticket,'form': form, 'id':id, 'uploaded_files': uploaded_files})

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
def ticket_list(request):
    if request.user.role < 3:
        mvm_tickets = MvmImport.objects.all()
        sielte_tickets = SielteImport.objects.all()
    if request.user.role == 3:
        mvm_tickets = MvmImport.objects.filter(assigned_to=request.user)
        sielte_tickets = SielteImport.objects.filter(assigned_to=request.user)
    tickets = list(chain(mvm_tickets, sielte_tickets))
    form_fields = {}
    form_fields['text'] = ''
    form_fields['status'] = ''
    form_fields['user'] = ''
    form_fields['end_date'] = ''
    form_fields['start_date'] = ''
    form = SearchForm(request.GET or None, request.FILES or None, initial=form_fields)

    start_date = datetime.datetime.now() - datetime.timedelta(60)
    end_date = datetime.datetime.now() + datetime.timedelta(60)
    date = '{} - {}'.format(start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y'))
    
    return render(request, 'ticket_list.html', {'title':'Lista ticket', 'tickets': tickets, 'form': form, 'date': date})

@login_required(login_url='/accounts/login/')
def search_tickets(request):
    form_fields = {}
    form_fields['text'] = ''
    form_fields['status'] = ''
    form_fields['user'] = ''

    form = SearchForm(request.GET or None, request.FILES or None, initial=form_fields)

    text = request.GET.get('text','')
    userpk = request.GET.get('user', '')
    status = request.GET.get('status', '')
    date = request.GET.get('date', '')

    mvm_queryset = Q()
    sielte_queryset = Q()

    if text:
        print("TEXT: " +text)
        mvm_queryset &= (Q(cod_wrid__icontains=text)|
        Q(keylavor__icontains=text)|
        Q(des_cogn__icontains=text)|
        Q(des_indi__icontains=text))
        sielte_queryset &= (
        Q(cod_wr_committente__icontains=text)|
        Q(nr__icontains=text)|
        Q(nome__icontains=text)|
        Q(indirizzo__icontains=text)
        )

    if userpk:
        user = User.objects.get(pk=userpk)
        print(user)
        mvm_queryset &= (Q(assigned_to=user))
        sielte_queryset &= (Q(assigned_to=user))

    if request.user.role == 3:
        user = User.objects.get(pk=request.user.pk)
        print(user)
        mvm_queryset &= (Q(assigned_to=user))
        sielte_queryset &= (Q(assigned_to=user))

    if status:
        print(status)
        if status != 'TUTTI':
            mvm_queryset &= (Q(status=status))
            sielte_queryset &= (Q(status=status))

    if date:
        start_date = datetime.datetime.strptime(date.split(' - ')[0], '%m/%d/%Y')
        end_date = datetime.datetime.strptime(date.split(' - ')[1], '%m/%d/%Y')
        mvm_queryset &= (
        Q(datainiz__gte=start_date)&
        Q(datainiz__lte=end_date)
        )

        sielte_queryset &= (
        Q(data_inizio_appuntamento__gte=start_date)&
        Q(data_inizio_appuntamento__lte=end_date)
        )

    mvm_tickets = MvmImport.objects.filter(mvm_queryset).distinct()
    sielte_tickets = SielteImport.objects.filter(sielte_queryset).distinct()
    tickets = list(chain(mvm_tickets, sielte_tickets))
    # for ticket in tickets:
    #     print(ticket)
    print(tickets)
    return render(request, 'ticket_list.html', {'title':'Lista ticket', 'tickets': tickets, 'form':form, 'date': date})

@login_required(login_url='/accounts/login/')
def save_mvm_ticket(request):
    pk = request.POST.get('id', '')
    print('PK: '+pk)

    mvm_ticket = MvmImport.objects.get(pk=pk)
    print(mvm_ticket)

    assigned_to = request.POST.get('assigned_to', '')
    if assigned_to:
        usr = User.objects.get(pk=assigned_to)
        if usr:
            mvm_ticket.assigned_to = usr


    note = request.POST.get('note', '')
    if note:
        mvm_ticket.note = note
        print(note)

    tipo_linea = request.POST.get('tipo_linea','')
    if tipo_linea:
        mvm_ticket.tipo_linea = tipo_linea
        print('TIPO LINEA: '+tipo_linea)

    stato_lavoro = request.POST.get('status','')
    if stato_lavoro:
        mvm_ticket.status = stato_lavoro
        print('STATO LAVORO: '+stato_lavoro)

    secondaria = request.POST.get('secondaria', '')
    if secondaria:
        mvm_ticket.secondaria = secondaria
        print('BOX: '+secondaria)

    derivato = request.POST.get('derivato', '')
    if derivato:
        mvm_ticket.derivato = derivato
        print('DERIVATO: '+derivato)

    presa = request.POST.get('presa', '')
    if presa:
        mvm_ticket.presa = presa
        print('PRESA: '+presa)

    cavetto = request.POST.get('cavetto', '')
    if cavetto:
        mvm_ticket.cavetto = cavetto
        print('CAVETTO: '+cavetto)

    tipologia_modem = request.POST.get('tipologia_modem', '')
    if tipologia_modem:
        mvm_ticket.tipologia_modem = tipologia_modem
        print('TIPOLOGIA MODEM: '+tipologia_modem)

    seriale_modem = request.POST.get('seriale_modem', '')
    if seriale_modem:
        mvm_ticket.seriale_modem = seriale_modem
        print('SERIALE MODEM: '+seriale_modem)


    if stato_lavoro == 'KO':
        motivo_ko = request.POST.get('motivo-ko', '')
        if motivo_ko:
            mvm_ticket.ko_reason = motivo_ko
            print('MOTIVO KO: '+motivo_ko)

    if tipo_linea == 'TRADIZIONALE':
        msan = request.POST.get('msan', '')
        if msan:
            mvm_ticket.msan = msan
            print('MSAN: '+msan)

        rete_rigida = request.POST.get('rete-rigida', '')
        if rete_rigida:
            mvm_ticket.rete_rigida = rete_rigida
            print('RETE RIGIDA: '+rete_rigida)

        cavo = request.POST.get('cavo', '')
        if cavo:
            mvm_ticket.cavo_cp_cavo = cavo
            print('CAVO: '+cavo)

        colonna = request.POST.get('colonna', '')
        if colonna:
            mvm_ticket.colonna = colonna
            print('COLONNA: '+colonna)

        cp_colonna = request.POST.get('cp-colonna', '')
        if cp_colonna:
            mvm_ticket.cp_col = cp_colonna
            print('CP COLONNA: '+cp_colonna)

        rl_trad = request.POST.get('rl', '')
        if rl_trad:
            mvm_ticket.rl = rl_trad
            print('RL TRADIZIONALE: '+rl_trad)

        cp_rl = request.POST.get('cp-rl', '')
        if cp_rl:
            mvm_ticket.cp_rl = cp_rl
            print('CP RL: '+cp_rl)

    if tipo_linea == 'FIBRA':
        rl_fibra = request.POST.get('rl', '')
        if rl_fibra:
            mvm_ticket.rl = rl_fibra
            print('RL FIBRA: '+rl_fibra)

        porta = request.POST.get('porta', '')
        if porta:
            mvm_ticket.porta = porta
            print('PORTA: '+porta)

    files = request.FILES.getlist('mvm-upload')
    if files:
        for f in files:
            cwd = os.getcwd()
            os.chdir('media')
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
            print(filename)
            uploaded_file_url = fs.url(filename)
            file = open(filename, 'rb')
            fileupload = UploadedFileMvm()
            fileupload.name = filename
            fileupload.file = File(file)
            fileupload.obj = mvm_ticket
            fileupload.save()
            os.chdir(cwd)



    mvm_ticket.save()


    return HttpResponseRedirect('/mvm-ticket/'+pk)


@login_required(login_url='/accounts/login/')
def save_sielte_ticket(request):
    pk = request.POST.get('id', '')
    print('PK: '+pk)

    sielte_ticket = SielteImport.objects.get(pk=pk)
    print(sielte_ticket)


    assigned_to = request.POST.get('assigned_to', '')
    if assigned_to:
        usr = User.objects.get(pk=assigned_to)
        if usr:
            sielte_ticket.assigned_to = usr
    
    stato_lavoro = request.POST.get('status','')
    if stato_lavoro:
        sielte_ticket.status = stato_lavoro
        print('STATO LAVORO: '+stato_lavoro)

    if stato_lavoro == 'KO':
        motivo_ko = request.POST.get('motivo-ko', '')
        if motivo_ko:
            sielte_ticket.ko_reason = motivo_ko
            print('MOTIVO KO: '+motivo_ko)

    note = request.POST.get('note', '')
    if note:
        sielte_ticket.note = note
        print(note)

    attivita = request.POST.get('attivita', '')
    if attivita:
        activity = SielteActivity.objects.get(servizio=attivita)
        sielte_ticket.attivita = activity
        print('ATTIVITA: '+attivita)

    attivita_agg = request.POST.get('attivita_aggiuntiva', '')
    if attivita:
        activity_agg = SielteExtraActivity.objects.get(servizio=attivita_agg)
        numero = request.POST.get('number', '')
        if numero:
            sielte_ticket.numero_agg = numero
        activity_agg.save()
        sielte_ticket.attivita_aggiuntiva = activity_agg
        print('ATTIVITA AGGIUNTIVA: '+attivita_agg)



    ora_da = request.POST.get('ora_da', '')
    if attivita:
        sielte_ticket.ora_da = ora_da
        print('ORA DA: '+ora_da)

    ora_a = request.POST.get('ora_a', '')
    if attivita:
        sielte_ticket.ora_a = ora_a
        print('ORA A: '+ora_a)


    files = request.FILES.getlist('sielte-upload')
    print(files)
    if files:
        for f in files:
            fs = FileSystemStorage()
            filename = fs.save(f.name, f)
            print(filename)
            uploaded_file_url = fs.url(filename)
            file = open('media/'+filename, 'rb')
            fileupload = UploadedFileSielte()
            fileupload.name = filename
            fileupload.file = File(file)
            fileupload.obj = sielte_ticket
            fileupload.save()


    sielte_ticket.save()

    return HttpResponseRedirect('/sielte-ticket/'+pk)








@login_required(login_url='/accounts/login/')
def import_page(request):
    return render(request, 'import.html', {'title':'Import'})

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
    return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

def strp_datetime_TZ(value):
    return strp_datetime_sielte(value[:value.rfind('.')].replace('T', ' '))

def strp_date(value):
    return datetime.datetime.strptime(value, '%Y-%m-%d')

def strp_time(value):
    return datetime.datetime.strptime(value, '%H:%M:%S')



@login_required(login_url='/accounts/login/')
def upload_mvm(request):
    file = request.FILES['mvm-import']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)

    with open('media/'+filename, 'rb+') as file:
        result = parse_mvm(file)

    return render(request, 'import_result.html', {'title':'Import', 'result':result})



@login_required(login_url='/accounts/login/')
def upload_sielte(request):
    file = request.FILES['sielte-import']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)

    with open('media/'+filename, 'rb+') as file:
        result = parse_sielte(file)

    return render(request, 'import.html', {'title':'Import'})

@login_required(login_url='/accounts/login/')
def upload_mvm_pdf(request):
    file = request.FILES['mvm-pdf']
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)

    with open('media/'+filename, 'rb+') as file:
        result = process_pdf(filename)

    return render(request, 'import_pdf_result.html', {'title':'Import', 'result': result})

def parse_mvm(file):
    xls = pd.ExcelFile(file)
    sheet = xls.parse(0, na_filter=False, dtype='object')
    records = sheet.to_dict(orient='records')
    result = {}
    row = 0
    for record in records:
        print(record)
        row += 1
        try:
            mvm = MvmImport()
            mvm.keylavor = record['keylavor']
            mvm.codicant = record['codicant']
            mvm.desccant = record['desccant']
            mvm.statprat = record['statprat']
            mvm.descstat = record['descstat']
            mvm.statfore = record['statfore']
            mvm.statback = record['statback']
            mvm.tipoprat = record['tipoprat']
            mvm.selezion = record['selezion']
            mvm.codiclie = record['codiclie']
            mvm.codiordi = record['codiordi']
            mvm.flagnwfm = record['flagnwfm']
            mvm.desctipo = record['desctipo']
            mvm.desclavo = record['desclavo']
            mvm.datainiz = strp_datetime(record['datainiz'])
            mvm.datafine = strp_datetime(record['datafine'])
            mvm.codinetw = record['codinetw']
            mvm.operazio = record['operazio']
            mvm.ordiacqu = record['ordiacqu']
            mvm.des_loca = record['des_loca']
            mvm.des_indi = record['des_indi']
            mvm.des_prov = record['des_prov']
            mvm.codisqua = record['codisqua']
            mvm.chiudato = strp_datetime(record['chiudato'])
            mvm.decantaz = record['decantaz']
            mvm.numetele = record['numetele']
            mvm.codelavo = clean(record['codelavo'])
            mvm.codicent = record['codicent']

            jobtype, created = MvmJob.objects.get_or_create(
                job_type=clean(record['job_type']),
            )
            mvm.job_type = jobtype

            mvm.desc_job = record['desc_job']
            mvm.datadisp = strp_datetime(record['datadisp'])
            mvm.prognazi = record['prognazi']
            mvm.des_cogn = record['des_cogn']
            mvm.cod_wrid = record['cod_wrid']
            mvm.appualle = strp_datetime(record['appualle'])
            mvm.appudall = strp_datetime(record['appudall'])
            mvm.stampata = record['stampata']
            mvm.invimail = record['invimail']
            mvm.desc_olo = record['desc_olo']
            mvm.ref_cogn = record['ref_cogn']
            mvm.ref_nome = record['ref_nome']
            mvm.reclamoc = record['reclamoc']
            mvm.systunic = record['systunic']
            mvm.numeripe = record['numeripe']
            mvm.numeretu = record['numeretu']
            mvm.ricez_dt = record['ricez_dt']
            mvm.prevriso = record['prevriso']
            mvm.campo001 = record['campo001']
            mvm.campo002 = record['campo002']
            mvm.selezio2 = record['selezio2']
            mvm.sla16_40 = record['sla16_40']
            mvm.sla16_70 = record['sla16_70']
            mvm.hours_40 = record['hours_40']
            mvm.hours_70 = record['hours_70']
            mvm.collaudo = record['collaudo']
            mvm.tipoprec = record['tipoprec']
            mvm.wfm_mira = record['wfm_mira']
            mvm.back_log = record['back_log']
            mvm.datascad = strp_datetime(record['datascad'])
            mvm.dataemis = strp_datetime(record['dataemis'])
            mvm.selevery = record['selevery']
            mvm.bloccata = record['bloccata']
            mvm.carat_wr = record['carat_wr']
            mvm.beginwor = strp_datetime(record['beginwor'])
            mvm.codfonte = record['codfonte']
            mvm.fore_job = record['fore_job']
            mvm.back_job = record['back_job']
            mvm.provscia = record['provscia']
            mvm.tipoback = record['tipoback']
            mvm.tipofore = record['tipofore']
            mvm.desc_pal = record['desc_pal']
            mvm.appu_old = record['appu_old']
            mvm.evolutio = record['evolutio']
            mvm.allegati = record['allegati']
            mvm.grup_sla = record['grup_sla']
            mvm.sollecit = record['sollecit']
            mvm.fullrepa = record['fullrepa']
            mvm.descomme = record['descomme']
            mvm.idwrprec = record['idwrprec']
            mvm.data_dad = record['data_dad']
            mvm.fasc_dad = record['fasc_dad']
            mvm.dataatti = strp_datetime(record['dataatti'])
            mvm.recaclie = record['recaclie']
            mvm.recacli1 = record['recacli1']
            mvm.rete_rig = record['rete_rig']
            mvm.codicavo = record['codicavo']
            mvm.codi_arm = record['codi_arm']
            mvm.repa_usc = record['repa_usc']
            mvm.decina = record['decina__']
            mvm.codi_box = record['codi_box']
            mvm.codiolia = record['codiolia']
            mvm.ades_npd = record['ades_npd']
            mvm.desc_isp = record['desc_isp']
            mvm.tiposwap = record['tiposwap']
            mvm.pratsuba = record['pratsuba']
            mvm.aggiorna = record['aggiorna']
            mvm.scadfest = record['scadfest']
            mvm.codaunic = record['codaunic']
            mvm.descsqua = record['descsqua']
            mvm.codisubb = record['codisubb']
            mvm.indimail = record['indimail']
            mvm.subadire = record['subadire']
            mvm.desccent = record['desccent']
            mvm.codiassi = record['codiassi']
            mvm.contexto = record['contexto']
            mvm.coditipo = record['coditipo']
            mvm.codicewr = record['codicewr']
            mvm.descassi = record['descassi']
            mvm.codidipe = record['codidipe']
            mvm.descdipe = record['descdipe']
            mvm.dipesuba = record['dipesuba']
            mvm.priority = record['priority']
            mvm.numetrim = record['numetrim']
            mvm.recolock = record['recolock']
            mvm.commitim = strp_datetime(record['commitim'])
            mvm.codi_aor = record['codi_aor']
            mvm.selechiu = record['selechiu']
            mvm.completa = strp_datetime(record['completa'])
            mvm.codi_isp = record['codi_isp']
            mvm.sla_xme = record['sla__xme']
            mvm.sla2_xme = record['sla2_xme']
            mvm.tota_sla = record['tota_sla']
            mvm.sla_nbd = record['sla__nbd']
            mvm.risvtele = record['risvtele']
            mvm.risvsqua = record['risvsqua']
            mvm.ripecavo = record['ripecavo']
            mvm.ripesqua = record['ripesqua']
            mvm.ripetele = record['ripetele']
            mvm.pos_dely = record['pos_dely']
            mvm.keylavw5 = record['keylavw5']
            mvm.lavormos = record['lavormos']
            mvm.tempolav = record['tempolav']
            mvm.squablok = record['squablok']
            mvm.response = record['response']
            mvm.dati_olo = record['dati_olo']
            mvm.codi_dtu = record['codi_dtu']
            mvm.slafonia = record['slafonia']
            mvm.colosla1 = record['colosla1']
            mvm.flussogc = record['flussogc']
            mvm.lavorata = record['lavorata']
            mvm.codiimpi = record['codiimpi']
            mvm.codicaus = record['codicaus']
            mvm.noteimpr = clean(record['noteimpr'])
            mvm.annotazi = clean(record['annotazi'])
            mvm.desclavb = clean(record['desclavb'])
            mvm.diagnosi = clean(record['diagnosi'])
            mvm.codirepa = record['codirepa']
            mvm.codirep2 = record['codirep2']
            mvm.codirep3 = record['codirep3']
            mvm.codisede = record['codisede']
            mvm.numepref = record['numepref']
            mvm.esitosub = record['esitosub']
            mvm.tempobbi = strp_datetime(record['tempobbi'])
            mvm.color_to = record['color_to']
            mvm.desc_aor = record['desc_aor']
            mvm.codi_aoa = record['codi_aoa']
            mvm.desc_aoa = record['desc_aoa']
            mvm.nopenale = record['nopenale']
            mvm.causobbi = record['causobbi']
            mvm.slakpid1 = record['slakpid1']
            mvm.slakpid4 = record['slakpid4']
            mvm.slak_d2a = record['slak_d2a']
            mvm.slak_d2b = record['slak_d2b']
            mvm.slak_d2c = record['slak_d2c']
            mvm.slak_d2d = record['slak_d2d']
            mvm.slak_d2e = record['slak_d2e']
            mvm.codicont = record['codicont']
            mvm.building = record['building']
            mvm.clli_roe = record['clli_roe']
            mvm.splitsec = record['splitsec']
            mvm.path_pop = record['path_pop']
            mvm.zonacent = record['zonacent']

            mvm_price, created = MvmPrice.objects.get_or_create(
                job_type=jobtype,
                desccent=record['desccent'],
            )
            mvm.price = mvm_price.price
            mvm.status = 'SOSPESO'

            repeat = MvmImport.objects.filter(codicent=record['codicent'], des_indi=record['des_indi'])
            print('REPEAT: '+str(len(repeat)))
            print(mvm)
            mvm.occorrenze = len(repeat)+1
            for r in repeat:
                r.occorrenze = len(repeat)+1
                r.save()

            mvm.save()
            result[row] = '{} caricato correttamente'.format(record['cod_wrid'])
        except:
            result[row] = '{} errore nel caricamento, controlla la riga {}'.format(record['cod_wrid'], row)

    return result

def parse_sielte(file):
    xls = pd.ExcelFile(file)
    sheet = xls.parse(0, na_filter=False, dtype='object')
    sheet = sheet.replace({pd.NaT: ''}).astype(str)
    records = sheet.to_dict(orient='records')
    result = {}
    row = 0
    for record in records:
        row += 1
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
            sielte.status = 'SOSPESO'

            # print(record['Tecnico Pratica'])
            # qui mi tocca fare una cafonata perché nell'export a volte
            # c'è scritto nome-cognome altre volte cognome-nome
            if record['Tecnico Pratica']:
                first_name = record['Tecnico Pratica'].split()[0]
                last_name = record['Tecnico Pratica'].split()[1]
                user = ''
                try:
                    user = User.objects.get(first_name=first_name, last_name=last_name)
                except:
                    try:
                        user = User.objects.get(first_name=last_name, last_name=first_name)
                    except:
                        pass
                if user:
                    sielte.assigned_to = user

            print(sielte)


            repeat = SielteImport.objects.filter(cod_centrale=record['Cod. Centrale'], indirizzo=record['Indirizzo'])
            print(repeat)
            print('REPEAT: '+str(len(repeat)))
            sielte.occorrenze = len(repeat)+1
            print(sielte)
            print('OCCURRENCES: ')
            for r in repeat:
                print(r)
                r.occorrenze = len(repeat)+1
                r.save()
            print('\n\n\n\n\n\n\n\n')
            sielte.save()
            result[row] = '{} caricato correttamente'.format(record['Cod. WR Committente'])
        except:
            result[row] = '{} errore nel caricamento, controlla la riga {}'.format(record['Cod. WR Committente'], row)

    return result

def pdf_splitter(path):
    with open(path, 'rb') as infile:
        reader = PdfFileReader(infile)
        for page in range(reader.getNumPages()):
            writer = PdfFileWriter()
            writer.addPage(reader.getPage(page))
            with open('media/mvm_pdf/splitted/{}.pdf'.format(page), 'wb') as outfile:
                writer.write(outfile)

def pdf_merge():
    mem = {}
    for filename in os.listdir('media/mvm_pdf/splitted'):
        print(filename)
        raw = parser.from_file('media/mvm_pdf/splitted/'+filename)
        for line in raw['content'].split('\n'):
            prs = ''.join(filter(str.isdigit, line))
            if 'WR: ' in line and len(prs) == 8:
                wr = prs
                print(wr)
                if wr not in mem.keys():
                    mem[wr] = {'filenames':[filename]}
                else:
                    l = mem[wr]['filenames']
                    l.append(filename)
                    mem[wr]['filenames'] = l
            if 'TEMPO OBIETTIVO' in line:
                tmpobb = line.replace('TEMPO OBIETTIVO -', '').strip()
                if wr not in mem.keys():
                    mem[wr] = {'tmpobb':tmpobb}
                else:
                    mem[wr]['tmpobb'] = tmpobb

    print(mem)
    for wr in mem.keys():
        pages = mem[wr]['filenames']
        pages.sort()
        print(pages)
        pdf = pdf_writer = PdfFileWriter()
        for page in pages:
            pdf_reader = PdfFileReader('media/mvm_pdf/splitted/{}'.format(page))
            pdf_writer.addPage(pdf_reader.getPage(0))
            with open('media/mvm_pdf/merged/{}-{}.pdf'.format(wr, mem[wr]['tmpobb']), 'wb') as fh:
                pdf_writer.write(fh)

def save_merged():
    cwd = os.getcwd()
    os.chdir('media/mvm_pdf/merged')
    result = {}
    for filename in os.listdir():
        wr = filename.split('-')[0]
        locale.setlocale(locale.LC_ALL, '')
        date = datetime.datetime.strptime(filename.split('-')[1].replace('.pdf', '').strip(), '%d %b %Y %H:%M:%S')
        try:
            mvm = MvmImport.objects.get(cod_wrid=wr, tempobbi=date)
            file = open(filename, 'rb')
            mvm.pdf_wr = File(file)
            mvm.save()
            result[wr] = 'pdf con codice wr {} salvato correttamente'.format(wr)
        except:
            result[wr] = 'non è stato possibile trovare ticket mvm con codice wr {} e tempo obiettivo {}'.format(wr, date)
    os.chdir(cwd)
    return result

def clear():
    for filename in os.listdir('media/mvm_pdf/splitted'):
        os.remove('media/mvm_pdf/splitted/'+filename)
    for filename in os.listdir('media/mvm_pdf/merged'):
        os.remove('media/mvm_pdf/merged/'+filename)
    for filename in os.listdir('media/'):
        if os.path.isfile('media/'+filename):
            os.remove('media/'+filename)

def process_pdf(file):
    pdf_splitter('media/'+file)
    pdf_merge()
    result = save_merged()
    clear()
    return result

@login_required(login_url='/accounts/login/')
def file_mvm_delete(request, ticket, id):
    file = UploadedFileMvm.objects.get(pk=id)
    file.delete()
    return HttpResponseRedirect('/mvm-ticket/'+str(ticket))

@login_required(login_url='/accounts/login/')
def file_sielte_delete(request, ticket, id):
    file = UploadedFileSielte.objects.get(pk=id)
    file.delete()
    return HttpResponseRedirect('/sielte-ticket/'+str(ticket))
