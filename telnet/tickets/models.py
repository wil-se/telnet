from django.db import models

# SE LA CHOICHE È CORTA LA METTO DIRETTAMENTE NELLA DICHIARAZIONE DEL CAMPO

descstat_choices = (
    ('ACQUISTE', 'ACQUISTE'),
    ('CHIUSE', 'CHIUSE'),
)

desctipo_choices = (
    ('NUOVI IMPIANTI ADSL', 'NUOVI IMPIANTI ADSL'),
    ('NUOVI IMPIANTI FONIA', 'NUOVI IMPIANTI FONIA'),
)

job_type_choices = (
    ('ERNCNINCAP', 'ERNCNINCAP'),
    ('ERRGRI-CAR', 'ERRGRI-CAR'),
    ('ERCTZSDAC', 'ERCTZSDAC'),
    ('ERNCRIN-AP', 'ERNCRIN-AP'),
    ('ERRANI-CA-', 'ERRANI-CA-'),
    ('ERNCTZNP-P', 'ERNCTZNP-P'),
    ('ERNCNINCCA', 'ERNCNINCCA'),
    ('ERADAC----', 'ERADAC----'),
    ('ERADNI-CA-', 'ERADNI-CA-'),
    ('ERRANI-CAR', 'ERRANI-CAR'),
    ('ERADTZ----', 'ERADTZ----'),
    ('ERURNI-CA-', 'ERURNI-CA-'),
    ('ERNCRI-CAR', 'ERNCRI-CAR'),
    ('ERRARI-U--', 'ERRARI-U--'),
)

desc_pal_choices = (
    ('ADSL', 'ADSL'),
    ('FONIA', 'FONIA'),
)

descrizione_tipologia_pratica_choices = (
    ('VF - Business', 'VF - Business'),
    ('FW - Business', 'FW - Business'),
    ('FW - Executive', 'FW - Executive'),
    ('TT', 'TT'),
    ('VF - Residenziale', 'VF - Residenziale'),
    ('FW - Braccialetti Elettronici', 'FW - Braccialetti Elettronici'),
    ('Adsl', 'Adsl'),
    ('FW - Manutenzioni Consip', 'FW - Manutenzioni Consip'),
    ('FW - Attivazioni Consip', 'FW - Attivazioni Consip'),
    ('Fonia', 'Fonia'),
    ('Progetti Speciali', 'Progetti Speciali')
)

nome_stato_choices = (
    ('New', 'New'),
    ('Nuovo', 'Nuovo'),
    ('Sospensione', 'Sospensione'),
    ('Working', 'Working'),
    ('Nuova', 'Nuova'),
    ('TRIAL - Appuntamento', 'TRIAL - Appuntamento'),
    ('In Lavorazione', 'In Lavorazione'),
    ('Da Lavorare', 'Da Lavorare'),
    ('TRIAL - Lavorabile', 'TRIAL - Lavorabile'),
    ('Programmata', 'Programmata'),
    ('Sospesa', 'Sospesa'),
    ('TRIAL - Sospeso', 'TRIAL - Sospeso')
)

tipo_cliente_choices = (
    ('Business', 'Business'),
    ('Residenziale', 'Residenziale')
)

mvm_status_choices = (
    ('OK', 'OK'),
    ('KO', 'KO'),
    ('SOSPESO', 'SOSPESO'),
    ('ANNULLATO', 'ANNULLATO'),
)

sielte_status_choices = (
    ('OK', 'OK'),
    ('KO', 'KO'),
    ('SOSPESO', 'SOSPESO'),
    ('ANNULLATO', 'ANNULLATO'),
    ('DA LAVORARE', 'DA LAVORARE'),
)

mvm_ko_choices = (
    ('TUBAZIONE-A14', 'TUBAZIONE PRIVATA A14'),
    ('TUBAZIONE-A24', 'TUBAZIONE PRIVATA A24'),
    ('CLT-IRREPERIBILE', 'CLT IRREPERIBILE'),
    ('RINUNCIA', 'RINUNCIA'),
    ('GENERICO', 'ECC. DISTANZA / GENERICO'),
)

sielte_ko_choices = (
    ('TUBAZIONE-A14', 'TUBAZIONE PRIVATA A14'),
    ('TUBAZIONE-A24', 'TUBAZIONE PRIVATA A24'),
    ('CLT-IRREPERIBILE', 'CLT IRREPERIBILE'),
    ('RINUNCIA', 'RINUNCIA'),
    ('GENERICO', 'ECC. DISTANZA / GENERICO'),
)

mvm_tipologia_modem_choices = (
    ('MODEM 100', 'MODEM 100'),
    ('MODEM 200', 'MODEM 200'),
    ('FRITZ BOX 7590', 'FRITZ BOX 7590'),
    ('FRITZ BOX 6890', 'FRITZ BOX 6890'),
    ('TIM BOX', 'TIM BOX'),
    ('MODEM PLUS', 'MODEM PLUS'),
)

cavetto_choices = (
    ('TRECCIOLA NUOVA', 'TRECCIOLA NUOVA'),
    ('TRECCIOLA ESISTENTE', 'TRECCIOLA ESISTENTE'),
    ('POLITENE NUOVA', 'POLITENE NUOVA'),
    ('POLITENE ESISTENTE', 'POLITENE ESISTENTE'),
    ('DROP NUOVA', 'DROP NUOVA'),
    ('DROP ESISTENTE', 'DROP ESISTENTE'),
)

class MvmImport(models.Model):
    keylavor = models.IntegerField(verbose_name="Key lavoro", default=0, blank=True, null=True)
    codicant = models.CharField(max_length=256, blank=True, null=True, default="")
    desccant = models.CharField(max_length=256, blank=True, null=True, default="")
    statprat = models.IntegerField(default=0, blank=True, null=True)
    descstat = models.CharField(choices=descstat_choices, max_length=256, blank=True, null=True, default="")
    statfore = models.IntegerField(default=0, blank=True, null=True)
    statback = models.IntegerField(default=0, blank=True, null=True)
    tipoprat = models.IntegerField(default=0, blank=True, null=True)
    selezion = models.IntegerField(default=0, blank=True, null=True)
    codiclie = models.CharField(max_length=256, blank=True, null=True, default="")
    codiordi = models.CharField(max_length=256, blank=True, null=True, default="")
    flagnwfm = models.IntegerField(default=0, blank=True, null=True)
    desctipo = models.CharField(choices=desctipo_choices, max_length=256, blank=True, null=True, default="")
    desclavo = models.CharField(max_length=256, blank=True, null=True, default="")
    datainiz = models.DateTimeField(blank=True, null=True)
    datafine = models.DateTimeField(blank=True, null=True)
    codinetw = models.CharField(max_length=256, blank=True, null=True, default="")
    operazio = models.CharField(max_length=256, blank=True, null=True, default="")
    ordiacqu = models.BigIntegerField(default=0, blank=True, null=True)
    des_loca = models.CharField(max_length=256, blank=True, null=True, default="")
    des_indi = models.CharField(max_length=256, blank=True, null=True, default="")
    des_prov = models.CharField(max_length=256, blank=True, null=True, default="")
    codisqua = models.CharField(max_length=256, blank=True, null=True, default="")
    chiudato = models.DateTimeField(blank=True, null=True)
    decantaz = models.IntegerField(default=0, blank=True, null=True)
    numetele = models.CharField(max_length=256, blank=True, null=True, default="")
    codelavo = models.IntegerField(default=0, blank=True, null=True)
    codicent = models.CharField(max_length=256, blank=True, null=True, default="")
    job_type = models.ForeignKey('MvmJob', default='JOB_MISSING', on_delete=models.SET_DEFAULT, blank=True, null=True)
    desc_job = models.CharField(max_length=256, blank=True, null=True, default="")
    datadisp = models.DateTimeField(blank=True, null=True)
    prognazi = models.CharField(max_length=256, blank=True, null=True, default="")
    des_cogn = models.CharField(max_length=256, blank=True, null=True, default="")
    cod_wrid = models.CharField(max_length=256, blank=True, null=True, default="")
    appualle = models.DateTimeField(blank=True, null=True)
    appudall = models.DateTimeField(blank=True, null=True)
    stampata = models.BooleanField(default=False)
    invimail = models.BooleanField(default=False)
    desc_olo = models.CharField(max_length=256, blank=True, null=True, default="")
    ref_cogn = models.CharField(max_length=256, blank=True, null=True, default="")
    ref_nome = models.CharField(max_length=256, blank=True, null=True, default="")
    reclamoc = models.CharField(max_length=256, blank=True, null=True, default="")
    systunic = models.CharField(max_length=10, blank=True, null=True, default="")
    numeripe = models.IntegerField(default=0, blank=True, null=True)
    numeretu = models.IntegerField(default=0, blank=True, null=True)
    ricez_dt = models.CharField(max_length=256, blank=True, null=True, default="")
    prevriso = models.CharField(max_length=256, blank=True, null=True, default="")
    campo001 = models.CharField(max_length=256, blank=True, null=True, default="")
    campo002 = models.CharField(max_length=256, blank=True, null=True, default="")
    selezio2 = models.IntegerField(default=0, blank=True, null=True)
    sla16_40 = models.CharField(max_length=1, blank=True, null=True, default="")
    sla16_70 = models.CharField(max_length=1, blank=True, null=True, default="")
    hours_40 = models.IntegerField(default=0, blank=True, null=True)
    hours_70 = models.IntegerField(default=0, blank=True, null=True)
    collaudo = models.BooleanField(default=False)
    tipoprec = models.CharField(max_length=256, blank=True, null=True, default="")
    wfm_mira = models.BooleanField(default=False)
    back_log = models.BooleanField(default=False)
    datascad = models.DateTimeField(blank=True, null=True)
    dataemis = models.DateTimeField(blank=True, null=True)
    selevery = models.BooleanField(default=False)
    bloccata = models.BooleanField(default=False)
    carat_wr = models.CharField(max_length=20, blank=True, null=True, default="")
    beginwor = models.DateTimeField(blank=True, null=True)
    codfonte = models.CharField(max_length=256, blank=True, null=True, default="")
    fore_job = models.BooleanField(default=False)
    back_job = models.BooleanField(default=False)
    provscia = models.BooleanField(default=False)
    tipoback = models.CharField(max_length=256, blank=True, null=True, default="")
    tipofore = models.CharField(max_length=256, blank=True, null=True, default="")
    desc_pal = models.CharField(choices=desc_pal_choices, max_length=256, blank=True, null=True, default="")
    appu_old = models.CharField(max_length=256, blank=True, null=True, default="")
    evolutio = models.BooleanField(default=False)
    allegati = models.BooleanField(default=False)
    grup_sla = models.BooleanField(default=False)
    sollecit = models.BooleanField(default=False)
    fullrepa = models.BooleanField(default=False)
    descomme = models.CharField(max_length=256, blank=True, null=True, default="")
    idwrprec = models.CharField(max_length=256, blank=True, null=True, default="")
    data_dad = models.CharField(max_length=256, blank=True, null=True, default="")
    fasc_dad = models.CharField(max_length=256, blank=True, null=True, default="")
    dataatti = models.DateTimeField(blank=True, null=True)
    recaclie = models.CharField(max_length=256, blank=True, null=True, default="")
    recacli1 = models.CharField(max_length=256, blank=True, null=True, default="")
    rete_rig = models.BooleanField(default=False)
    codicavo = models.CharField(max_length=256, blank=True, null=True, default="")
    codi_arm = models.CharField(max_length=256, blank=True, null=True, default="")
    repa_usc = models.CharField(max_length=256, blank=True, null=True, default="")
    decina = models.CharField(max_length=256, blank=True, null=True, default="")
    codi_box = models.CharField(max_length=256, blank=True, null=True, default="")
    codiolia = models.CharField(max_length=256, blank=True, null=True, default="")
    ades_npd = models.BooleanField(default=False)
    desc_isp = models.CharField(max_length=256, blank=True, null=True, default="")
    tiposwap = models.BooleanField(default=False)
    pratsuba = models.BooleanField(default=False)
    aggiorna = models.BooleanField(default=False)
    scadfest = models.BooleanField(default=False)
    codaunic = models.BooleanField(default=False)
    descsqua = models.CharField(max_length=256, blank=True, null=True, default="")
    codisubb = models.BooleanField(default=False)
    indimail = models.CharField(max_length=256, blank=True, null=True, default="")
    subadire = models.BooleanField(default=False)
    desccent = models.CharField(max_length=256, blank=True, null=True, default="")
    codiassi = models.CharField(max_length=8, blank=True, null=True, default="")
    contexto = models.CharField(max_length=256, blank=True, null=True, default="")
    coditipo = models.CharField(max_length=256, blank=True, null=True, default="")
    codicewr = models.CharField(max_length=20, blank=True, null=True, default="")
    descassi = models.CharField(max_length=256, blank=True, null=True, default="")
    codidipe = models.CharField(max_length=256, blank=True, null=True, default="")
    descdipe = models.CharField(max_length=256, blank=True, null=True, default="")
    dipesuba = models.CharField(max_length=256, blank=True, null=True, default="")
    priority = models.BooleanField(default=False)
    numetrim = models.IntegerField(default=0, blank=True, null=True)
    recolock = models.CharField(max_length=256, blank=True, null=True, default="")
    commitim = models.DateTimeField(blank=True, null=True)
    codi_aor = models.CharField(max_length=4, blank=True, null=True, default="")
    selechiu = models.BooleanField(default=False)
    completa = models.DateTimeField(blank=True, null=True)
    codi_isp = models.CharField(max_length=8, blank=True, null=True, default="")
    sla_xme = models.IntegerField(default=0, blank=True, null=True)
    sla2_xme = models.BooleanField(default=False)
    tota_sla = models.IntegerField(default=0, blank=True, null=True)
    sla_nbd = models.BooleanField(default=False)
    risvtele = models.CharField(max_length=256, blank=True, null=True, default="")
    risvsqua = models.CharField(max_length=256, blank=True, null=True, default="")
    ripecavo = models.CharField(max_length=256, blank=True, null=True, default="")
    ripesqua = models.CharField(max_length=256, blank=True, null=True, default="")
    ripetele = models.CharField(max_length=256, blank=True, null=True, default="")
    pos_dely = models.CharField(max_length=256, blank=True, null=True, default="")
    keylavw5 = models.CharField(max_length=7, blank=True, null=True, default="")
    lavormos = models.BooleanField(default=False)
    tempolav = models.IntegerField(default=0, blank=True, null=True)
    squablok = models.BooleanField(default=False)
    response = models.CharField(max_length=3, blank=True, null=True, default="")
    dati_olo = models.CharField(max_length=1, blank=True, null=True, default="")
    slafonia = models.IntegerField(default=0, blank=True, null=True)
    codi_dtu = models.CharField(max_length=13, blank=True, null=True, default="")
    colosla1 = models.CharField(max_length=8, blank=True, null=True, default="")
    flussogc = models.CharField(max_length=256, blank=True, null=True, default="")
    codiimpi = models.CharField(max_length=6, blank=True, null=True, default="")
    lavorata = models.BooleanField(default=False)
    codicaus = models.CharField(max_length=256, blank=True, null=True, default="")
    noteimpr = models.CharField(max_length=512, blank=True, null=True, default="")
    annotazi = models.TextField(max_length=512, blank=True, null=True, default="")
    desclavb = models.TextField(max_length=512, blank=True, null=True, default="")
    diagnosi = models.CharField(max_length=256, blank=True, null=True, default="")
    codirepa = models.CharField(max_length=4, blank=True, null=True, default="")
    codirep2 = models.CharField(max_length=4, blank=True, null=True, default="")
    codirep3 = models.CharField(max_length=4, blank=True, null=True, default="")
    codisede = models.CharField(max_length=256, blank=True, null=True, default="")
    numepref = models.CharField(max_length=8, blank=True, null=True, default="")
    esitosub = models.BooleanField(default=False)
    tempobbi = models.DateTimeField(blank=True, null=True)
    color_to = models.IntegerField(default=0, blank=True, null=True)
    desc_aor = models.CharField(max_length=256, blank=True, null=True, default="")
    codi_aoa = models.CharField(max_length=256, blank=True, null=True, default="")
    desc_aoa = models.CharField(max_length=256, blank=True, null=True, default="")
    nopenale = models.BooleanField(default=False)
    causobbi = models.CharField(max_length=256, blank=True, null=True, default="")
    slakpid1 = models.BooleanField(default=False)
    slakpid4 = models.BooleanField(default=False)
    slak_d2a = models.BooleanField(default=False)
    slak_d2b = models.BooleanField(default=False)
    slak_d2c = models.BooleanField(default=False)
    slak_d2d = models.BooleanField(default=False)
    slak_d2e = models.BooleanField(default=False)
    codicont = models.CharField(max_length=10, blank=True, null=True, default="")
    building = models.CharField(max_length=256, blank=True, null=True, default="")
    clli_roe = models.CharField(max_length=256, blank=True, null=True, default="")
    splitsec = models.CharField(max_length=256, blank=True, null=True, default="")
    path_pop = models.CharField(max_length=256, blank=True, null=True, default="")
    zonacent = models.CharField(max_length=1, blank=True, null=True, default="")

    # campi oltre quelli importati
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    assigned_to = models.ForeignKey('authentication.User', default=None, on_delete=models.SET_DEFAULT, blank=True, null=True)
    cod_modem = models.CharField(max_length=256, blank=True, null=True, default="")
    note = models.TextField(max_length=2048, blank=True, null=True)
    tipologia_modem = models.CharField(choices=mvm_tipologia_modem_choices, max_length=256, blank=True, null=True, default="")
    seriale_modem = models.CharField(max_length=256, blank=True, null=True, default="")

    # TIPO LINEA
    tipo_linea = models.CharField(verbose_name='Tipo linea', choices=(('TRADIZIONALE', 'TRADIZIONALE'),('FIBRA', 'FIBRA')), max_length=256, blank=True, null=True)
    status = models.CharField(verbose_name='Stato lavoro', choices=mvm_status_choices, max_length=256, blank=True, null=True)
    ko_reason = models.CharField(verbose_name='Motivo KO', choices=mvm_ko_choices, max_length=256, blank=True, null=True)
    msan = models.CharField(verbose_name='Msan', max_length=256, blank=True, null=True)
    rete_rigida = models.CharField(verbose_name='Rete rigida', choices=(('SI', 'SI'),('NO', 'NO')),  max_length=256, blank=True, null=True)
    cavo_cp_cavo = models.CharField(verbose_name='Cavo', max_length=256, blank=True, null=True)
    colonna_cp_colonna = models.CharField(verbose_name='Colonna', max_length=256, blank=True, null=True)
    rl_cp_rl = models.CharField(verbose_name='Rl', max_length=256, blank=True, null=True)
    secondaria = models.CharField(verbose_name='Secondaria', max_length=256, blank=True, null=True)    
    derivato = models.IntegerField(verbose_name='Derivato', default=0, blank=True, null=True)
    presa = models.CharField(verbose_name='Presa', max_length=256, blank=True, null=True)
    cavetto = models.CharField(verbose_name='Cavetto', choices=cavetto_choices,  max_length=256, blank=True, null=True)
    stato_cavo = models.CharField(verbose_name='Stato cavo', max_length=256, choices=(('NUOVA POSA', 'NUOVA POSA'),('ESISTENTE', 'ESISTENTE')), blank=True, null=True )
    porta = models.CharField(verbose_name='Porta', max_length=256, blank=True, null=True)
    occorrenze = models.IntegerField(default=1, blank=True, null=True)
    pdf_wr = models.FileField(upload_to ='mvm_wr_pdf', blank=True, null=True)

    def __str__(self):
        return 'MVM {} {} {}'.format(self.cod_wrid, self.job_type, self.desctipo, self.des_loca)

    class Meta:
        verbose_name = 'Mvm import'
        verbose_name_plural = 'Mvm imports'


class SielteImport(models.Model):
    cod_wr_committente = models.CharField(max_length=256, blank=True, null=True, default="")
    impianto = models.CharField(max_length=256, blank=True, null=True, default="")
    descrizione_centrale = models.CharField(max_length=256, blank=True, null=True, default="")
    nome = models.CharField(max_length=256, blank=True, null=True, default="")
    indirizzo = models.CharField(max_length=256, blank=True, null=True, default="")
    descrizione_tipologia_pratica = models.CharField(choices=descrizione_tipologia_pratica_choices, max_length=256, blank=True, null=True, default="")
    nome_assistente = models.CharField(max_length=256, blank=True, null=True, default="")
    tecnico_pratica = models.CharField(max_length=256, blank=True, null=True, default="")
    data_inizio_appuntamento = models.DateField(max_length=256, blank=True, null=True) # 12/08/2020
    ora_inizio_appuntamento = models.TimeField(max_length=256, blank=True, null=True) # 12:00:00
    descrizione_pratica = models.CharField(max_length=256, blank=True, null=True, default="")
    nr = models.CharField(max_length=256, blank=True, null=True, default="")
    cod_stato = models.CharField(max_length=256, blank=True, null=True, default="")
    nome_stato = models.CharField(choices=nome_stato_choices, max_length=256, blank=True, null=True, default="")
    tempo_di_esecuzione = models.IntegerField(blank=True, null=True)
    cod_centrale = models.CharField(max_length=256, blank=True, null=True, default="")
    codice_progetto = models.CharField(max_length=256, blank=True, null=True, default="")
    citta = models.CharField(max_length=256, blank=True, null=True, default="")
    provincia = models.CharField(max_length=256, blank=True, null=True, default="")
    data_di_ricezione = models.DateTimeField(max_length=256, blank=True, null=True) # 2020-08-10T10:37:03.56Z
    aging = models.CharField(max_length=256, blank=True, null=True, default="")
    data_scadenza = models.DateField(max_length=256, blank=True, null=True) # 29/08/2020
    data_appuntamento_a = models.DateField(max_length=256, blank=True, null=True) # 10/08/2020
    ora_fine_appuntamento = models.TimeField(max_length=256, blank=True, null=True) # 19:00:00
    inizio_lavorazione_prevista = models.DateTimeField(max_length=256, blank=True, null=True) # 2020-08-11T08:00:00Z
    fine_lavorazione_prevista = models.DateTimeField(max_length=256, blank=True, null=True) # 2020-08-11T09:00:00Z
    data_chiusura = models.DateField(max_length=256, blank=True, null=True)
    ora_chiusura = models.TimeField(max_length=256, blank=True, null=True)
    telefono_cliente_1 = models.CharField(max_length=256, blank=True, null=True, default="")
    telefono_cliente_2 = models.CharField(max_length=256, blank=True, null=True, default="")
    riferimento_cliente = models.CharField(max_length=256, blank=True, null=True, default="")
    nr_occorrenze = models.IntegerField(blank=True, null=True)
    e_mail = models.CharField(max_length=256, blank=True, null=True, default="")
    identificativo_cliente = models.CharField(max_length=256, blank=True, null=True, default="")
    nome_ubicazione = models.CharField(max_length=256, blank=True, null=True, default="")
    pratica_chiusa = models.BooleanField(default=False)
    pratica_interna = models.BooleanField(default=False)
    pratica_nuova = models.BooleanField(default=False)
    tipo_cliente = models.CharField(choices=tipo_cliente_choices, max_length=256, blank=True, null=True, default="")
    tipo_telefono_1 = models.CharField(max_length=256, blank=True, null=True, default="")
    tipo_telefono_2 = models.CharField(max_length=256, blank=True, null=True, default="")

    # campi oltre quelli importati
    assigned_to = models.ForeignKey('authentication.User', default=None, on_delete=models.SET_DEFAULT, blank=True, null=True)
    status = models.CharField(choices=sielte_status_choices, default='SOSPESO', max_length=256, blank=True, null=True)
    note = models.TextField(max_length=2048, blank=True, null=True)

    attivita = models.ForeignKey('SielteActivity', default=None, on_delete=models.SET_DEFAULT, blank=True, null=True)
    attivita_aggiuntiva = models.ForeignKey('SielteExtraActivity', default=None, on_delete=models.SET_DEFAULT, blank=True, null=True)
    status = models.CharField(verbose_name='Stato lavoro', choices=sielte_status_choices, max_length=256, blank=True, null=True)
    ko_reason = models.CharField(verbose_name='Motivo KO', choices=sielte_ko_choices, max_length=256, blank=True, null=True)
    ora_da = models.TimeField(max_length=256, blank=True, null=True)
    ora_a = models.TimeField(max_length=256, blank=True, null=True)
    numero_agg = models.IntegerField(default=1, blank=True, null=True)
    occorrenze = models.IntegerField(default=1, blank=True, null=True)
    
    tot_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return 'SIELTE {} {} {}'.format(self.cod_wr_committente, self.cod_centrale, self.nome,)

    class Meta:
        verbose_name = 'Sielte import'
        verbose_name_plural = 'Sielte imports'
    
    def save(self, *args, **kwargs):
        gain = 0
        if self.attivita and self.attivita.guadagno:
            gain += int(self.attivita.guadagno)
        
        if self.attivita_aggiuntiva and self.attivita_aggiuntiva.guadagno and self.numero_agg:
            gain += int(self.attivita_aggiuntiva.guadagno) * int(self.numero_agg)

        self.tot_price = gain

        # print("saving Sielte import, tot price {}".format(gain))

        super(SielteImport, self).save(*args, **kwargs)


# date una città e un codice lavoro esiste un prezzo associato
# queste informazioni sono presenti in una tabella excel
# e vengono usate durante l'import di mvm

class MvmJob(models.Model):
    job_type = models.CharField(max_length=256, primary_key=True)

    def __str__(self):
        return self.job_type

    class Meta:
        verbose_name = 'Mvm job type'
        verbose_name_plural = 'Mvm job types'


class MvmPrice(models.Model):
    job_type = models.ForeignKey('MvmJob', default='JOB_MISSING', on_delete=models.SET_DEFAULT)
    desccent = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.job_type, self.desccent, self.price)

    class Meta:
        verbose_name = 'Mvm price'
        verbose_name_plural = 'Mvm prices'
        unique_together = (('job_type', 'desccent'),)


class SielteActivity(models.Model):
    servizio = models.CharField(max_length=256, primary_key=True)
    guadagno = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.servizio)

    class Meta:
        verbose_name = 'Sielte activity'
        verbose_name_plural = 'Sielte activity'


class SielteExtraActivity(models.Model):
    servizio = models.CharField(max_length=256, primary_key=True)
    guadagno = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return '{}'.format(self.servizio)

    class Meta:
        verbose_name = 'Sielte Extra activity'
        verbose_name_plural = 'Sielte Extra activities'


class UploadedFileMvm(models.Model):
    obj = models.ForeignKey('MvmImport', default='OBJ_MISSING', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to ='file_uploads_mvm')

class UploadedFileSielte(models.Model):
    obj = models.ForeignKey('SielteImport', default='OBJ_MISSING', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to ='file_uploads_sielte')

class MvmExport(models.Model):
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to ='mvm_export')

class SielteExport(models.Model):
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to ='sielte_export')