from django.db import models


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


sielte_status_choices = (
    ('OK', 'OK'),
    ('KO', 'KO'),
    ('SOSPESO', 'SOSPESO'),
    ('ANNULLATO', 'ANNULLATO'),
    ('DA LAVORARE', 'DA LAVORARE'),
)

sielte_ko_choices = (
    ('TUBAZIONE-A14', 'TUBAZIONE PRIVATA A14'),
    ('TUBAZIONE-A24', 'TUBAZIONE PRIVATA A24'),
    ('CLT-IRREPERIBILE', 'CLT IRREPERIBILE'),
    ('RINUNCIA', 'RINUNCIA'),
    ('GENERICO', 'ECC. DISTANZA / GENERICO'),
)


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
    mail = models.CharField(max_length=256, blank=True, null=True, default="")
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
        return 'SIELTE {} {} {}'.format(self.nr, self.cod_centrale, self.nome,)

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


class UploadedFileSielte(models.Model):
    obj = models.ForeignKey('SielteImport', default='OBJ_MISSING', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to ='file_uploads_sielte')


class SielteExport(models.Model):
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to ='sielte_export')