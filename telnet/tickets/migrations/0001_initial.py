# Generated by Django 3.1.1 on 2020-09-20 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MvmImport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keylavor', models.IntegerField(blank=True, default=0, null=True, verbose_name='Key lavoro')),
                ('codicant', models.CharField(blank=True, max_length=256, null=True)),
                ('desccant', models.CharField(blank=True, max_length=256, null=True)),
                ('statprat', models.IntegerField(blank=True, default=0, null=True)),
                ('descstat', models.CharField(blank=True, choices=[('ACQUISTE', 'ACQUISTE'), ('CHIUSE', 'CHIUSE')], max_length=256, null=True)),
                ('statfore', models.IntegerField(blank=True, default=0, null=True)),
                ('statback', models.IntegerField(blank=True, default=0, null=True)),
                ('tipoprat', models.IntegerField(blank=True, default=0, null=True)),
                ('selezion', models.IntegerField(blank=True, default=0, null=True)),
                ('codiclie', models.CharField(blank=True, max_length=256, null=True)),
                ('codiordi', models.CharField(blank=True, max_length=256, null=True)),
                ('flagnwfm', models.IntegerField(blank=True, default=0, null=True)),
                ('desctipo', models.CharField(blank=True, choices=[('NUOVI IMPIANTI ADSL', 'NUOVI IMPIANTI ADSL'), ('NUOVI IMPIANTI FONIA', 'NUOVI IMPIANTI FONIA')], max_length=256, null=True)),
                ('desclavo', models.CharField(blank=True, max_length=256, null=True)),
                ('datainiz', models.DateTimeField(blank=True, null=True)),
                ('datafine', models.DateTimeField(blank=True, null=True)),
                ('codinetw', models.CharField(blank=True, max_length=256, null=True)),
                ('operazio', models.CharField(blank=True, max_length=256, null=True)),
                ('ordiacqu', models.BigIntegerField(blank=True, default=0, null=True)),
                ('des_loca', models.CharField(blank=True, max_length=256, null=True)),
                ('des_indi', models.CharField(blank=True, max_length=256, null=True)),
                ('des_prov', models.CharField(blank=True, max_length=256, null=True)),
                ('codisqua', models.CharField(blank=True, max_length=256, null=True)),
                ('chiudato', models.DateTimeField(blank=True, null=True)),
                ('decantaz', models.IntegerField(blank=True, default=0, null=True)),
                ('numetele', models.CharField(blank=True, max_length=256, null=True)),
                ('codelavo', models.IntegerField(blank=True, default=0, null=True)),
                ('codicent', models.CharField(blank=True, max_length=256, null=True)),
                ('desc_job', models.CharField(blank=True, max_length=256, null=True)),
                ('datadisp', models.DateTimeField(blank=True, null=True)),
                ('prognazi', models.CharField(blank=True, max_length=256, null=True)),
                ('des_cogn', models.CharField(blank=True, max_length=256, null=True)),
                ('cod_wrid', models.CharField(blank=True, max_length=256, null=True)),
                ('appualle', models.DateTimeField(blank=True, null=True)),
                ('appudall', models.DateTimeField(blank=True, null=True)),
                ('stampata', models.BooleanField(default=False)),
                ('invimail', models.BooleanField(default=False)),
                ('desc_olo', models.CharField(blank=True, max_length=256, null=True)),
                ('ref_cogn', models.CharField(blank=True, max_length=256, null=True)),
                ('ref_nome', models.CharField(blank=True, max_length=256, null=True)),
                ('reclamoc', models.CharField(blank=True, max_length=256, null=True)),
                ('systunic', models.CharField(blank=True, max_length=10, null=True)),
                ('numeripe', models.IntegerField(blank=True, default=0, null=True)),
                ('numeretu', models.IntegerField(blank=True, default=0, null=True)),
                ('ricez_dt', models.CharField(blank=True, max_length=256, null=True)),
                ('prevriso', models.CharField(blank=True, max_length=256, null=True)),
                ('campo001', models.CharField(blank=True, max_length=256, null=True)),
                ('campo002', models.CharField(blank=True, max_length=256, null=True)),
                ('selezio2', models.IntegerField(blank=True, default=0, null=True)),
                ('sla16_40', models.CharField(blank=True, max_length=1, null=True)),
                ('sla16_70', models.CharField(blank=True, max_length=1, null=True)),
                ('hours_40', models.IntegerField(blank=True, default=0, null=True)),
                ('hours_70', models.IntegerField(blank=True, default=0, null=True)),
                ('collaudo', models.BooleanField(default=False)),
                ('tipoprec', models.CharField(blank=True, max_length=256, null=True)),
                ('wfm_mira', models.BooleanField(default=False)),
                ('back_log', models.BooleanField(default=False)),
                ('datascad', models.DateTimeField(blank=True, null=True)),
                ('dataemis', models.DateTimeField(blank=True, null=True)),
                ('selevery', models.BooleanField(default=False)),
                ('bloccata', models.BooleanField(default=False)),
                ('carat_wr', models.CharField(blank=True, max_length=20, null=True)),
                ('beginwor', models.DateTimeField(blank=True, null=True)),
                ('codfonte', models.CharField(blank=True, max_length=256, null=True)),
                ('fore_job', models.BooleanField(default=False)),
                ('back_job', models.BooleanField(default=False)),
                ('provscia', models.BooleanField(default=False)),
                ('tipoback', models.CharField(blank=True, max_length=256, null=True)),
                ('tipofore', models.CharField(blank=True, max_length=256, null=True)),
                ('desc_pal', models.CharField(blank=True, choices=[('ADSL', 'ADSL'), ('FONIA', 'FONIA')], max_length=256, null=True)),
                ('appu_old', models.CharField(blank=True, max_length=256, null=True)),
                ('evolutio', models.BooleanField(default=False)),
                ('allegati', models.BooleanField(default=False)),
                ('grup_sla', models.BooleanField(default=False)),
                ('sollecit', models.BooleanField(default=False)),
                ('fullrepa', models.BooleanField(default=False)),
                ('descomme', models.CharField(blank=True, max_length=256, null=True)),
                ('idwrprec', models.CharField(blank=True, max_length=256, null=True)),
                ('data_dad', models.CharField(blank=True, max_length=256, null=True)),
                ('fasc_dad', models.CharField(blank=True, max_length=256, null=True)),
                ('dataatti', models.DateTimeField(blank=True, null=True)),
                ('recaclie', models.CharField(blank=True, max_length=256, null=True)),
                ('recacli1', models.CharField(blank=True, max_length=256, null=True)),
                ('rete_rig', models.BooleanField(default=False)),
                ('codicavo', models.CharField(blank=True, max_length=256, null=True)),
                ('codi_arm', models.CharField(blank=True, max_length=256, null=True)),
                ('repa_usc', models.CharField(blank=True, max_length=256, null=True)),
                ('decina', models.CharField(blank=True, max_length=256, null=True)),
                ('codi_box', models.CharField(blank=True, max_length=256, null=True)),
                ('codiolia', models.CharField(blank=True, max_length=256, null=True)),
                ('ades_npd', models.BooleanField(default=False)),
                ('desc_isp', models.CharField(blank=True, max_length=256, null=True)),
                ('tiposwap', models.BooleanField(default=False)),
                ('pratsuba', models.BooleanField(default=False)),
                ('aggiorna', models.BooleanField(default=False)),
                ('scadfest', models.BooleanField(default=False)),
                ('codaunic', models.BooleanField(default=False)),
                ('descsqua', models.CharField(blank=True, max_length=256, null=True)),
                ('codisubb', models.BooleanField(default=False)),
                ('indimail', models.CharField(blank=True, max_length=256, null=True)),
                ('subadire', models.BooleanField(default=False)),
                ('desccent', models.CharField(blank=True, max_length=256, null=True)),
                ('codiassi', models.CharField(blank=True, max_length=8, null=True)),
                ('contexto', models.CharField(blank=True, max_length=256, null=True)),
                ('coditipo', models.CharField(blank=True, max_length=256, null=True)),
                ('codicewr', models.CharField(blank=True, max_length=20, null=True)),
                ('descassi', models.CharField(blank=True, max_length=256, null=True)),
                ('codidipe', models.CharField(blank=True, max_length=256, null=True)),
                ('descdipe', models.CharField(blank=True, max_length=256, null=True)),
                ('dipesuba', models.CharField(blank=True, max_length=256, null=True)),
                ('priority', models.BooleanField(default=False)),
                ('numetrim', models.IntegerField(blank=True, default=0, null=True)),
                ('recolock', models.CharField(blank=True, max_length=256, null=True)),
                ('commitim', models.DateTimeField(blank=True, null=True)),
                ('codi_aor', models.CharField(blank=True, max_length=4, null=True)),
                ('selechiu', models.BooleanField(default=False)),
                ('completa', models.DateTimeField(blank=True, null=True)),
                ('codi_isp', models.CharField(blank=True, max_length=8, null=True)),
                ('sla_xme', models.IntegerField(blank=True, default=0, null=True)),
                ('sla2_xme', models.BooleanField(default=False)),
                ('tota_sla', models.IntegerField(blank=True, default=0, null=True)),
                ('sla_nbd', models.BooleanField(default=False)),
                ('risvtele', models.CharField(blank=True, max_length=256, null=True)),
                ('risvsqua', models.CharField(blank=True, max_length=256, null=True)),
                ('ripecavo', models.CharField(blank=True, max_length=256, null=True)),
                ('ripesqua', models.CharField(blank=True, max_length=256, null=True)),
                ('ripetele', models.CharField(blank=True, max_length=256, null=True)),
                ('pos_dely', models.CharField(blank=True, max_length=256, null=True)),
                ('keylavw5', models.CharField(blank=True, max_length=7, null=True)),
                ('lavormos', models.BooleanField(default=False)),
                ('tempolav', models.IntegerField(blank=True, default=0, null=True)),
                ('squablok', models.BooleanField(default=False)),
                ('response', models.CharField(blank=True, max_length=3, null=True)),
                ('dati_olo', models.CharField(blank=True, max_length=1, null=True)),
                ('slafonia', models.IntegerField(blank=True, default=0, null=True)),
                ('codi_dtu', models.CharField(blank=True, max_length=13, null=True)),
                ('colosla1', models.CharField(blank=True, max_length=8, null=True)),
                ('flussogc', models.CharField(blank=True, max_length=256, null=True)),
                ('codiimpi', models.CharField(blank=True, max_length=6, null=True)),
                ('lavorata', models.BooleanField(default=False)),
                ('codicaus', models.CharField(blank=True, max_length=256, null=True)),
                ('noteimpr', models.CharField(blank=True, max_length=512, null=True)),
                ('annotazi', models.TextField(blank=True, max_length=512, null=True)),
                ('desclavb', models.TextField(blank=True, max_length=512, null=True)),
                ('diagnosi', models.CharField(blank=True, max_length=256, null=True)),
                ('codirepa', models.CharField(blank=True, max_length=4, null=True)),
                ('codirep2', models.CharField(blank=True, max_length=4, null=True)),
                ('codirep3', models.CharField(blank=True, max_length=4, null=True)),
                ('codisede', models.CharField(blank=True, max_length=256, null=True)),
                ('numepref', models.CharField(blank=True, max_length=8, null=True)),
                ('esitosub', models.BooleanField(default=False)),
                ('tempobbi', models.DateTimeField(blank=True, null=True)),
                ('color_to', models.IntegerField(blank=True, default=0, null=True)),
                ('desc_aor', models.CharField(blank=True, max_length=256, null=True)),
                ('codi_aoa', models.CharField(blank=True, max_length=256, null=True)),
                ('desc_aoa', models.CharField(blank=True, max_length=256, null=True)),
                ('nopenale', models.BooleanField(default=False)),
                ('causobbi', models.CharField(blank=True, max_length=256, null=True)),
                ('slakpid1', models.BooleanField(default=False)),
                ('slakpid4', models.BooleanField(default=False)),
                ('slak_d2a', models.BooleanField(default=False)),
                ('slak_d2b', models.BooleanField(default=False)),
                ('slak_d2c', models.BooleanField(default=False)),
                ('slak_d2d', models.BooleanField(default=False)),
                ('slak_d2e', models.BooleanField(default=False)),
                ('codicont', models.CharField(blank=True, max_length=10, null=True)),
                ('building', models.CharField(blank=True, max_length=256, null=True)),
                ('clli_roe', models.CharField(blank=True, max_length=256, null=True)),
                ('splitsec', models.CharField(blank=True, max_length=256, null=True)),
                ('path_pop', models.CharField(blank=True, max_length=256, null=True)),
                ('zonacent', models.CharField(blank=True, max_length=1, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cod_modem', models.CharField(blank=True, max_length=256, null=True)),
                ('note', models.TextField(blank=True, max_length=2048, null=True)),
                ('tipologia_modem', models.CharField(blank=True, choices=[('MODEM 100', 'MODEM 100'), ('MODEM 200', 'MODEM 200'), ('FRITZ BOX 7590', 'FRITZ BOX 7590'), ('FRITZ BOX 6890', 'FRITZ BOX 6890'), ('TIM BOX', 'TIM BOX'), ('MODEM PLUS', 'MODEM PLUS')], max_length=256, null=True)),
                ('seriale_modem', models.CharField(blank=True, max_length=256, null=True)),
                ('tipo_linea', models.CharField(blank=True, choices=[('TRADIZIONALE', 'TRADIZIONALE'), ('FIBRA', 'FIBRA')], max_length=256, null=True, verbose_name='Tipo linea')),
                ('status', models.CharField(blank=True, choices=[('OK', 'OK'), ('KO', 'KO'), ('SOSPESO', 'SOSPESO'), ('ANNULLATO', 'ANNULLATO')], max_length=256, null=True, verbose_name='Stato lavoro')),
                ('ko_reason', models.CharField(blank=True, choices=[('TUBAZIONE-A14', 'TUBAZIONE PRIVATA A14'), ('TUBAZIONE-A24', 'TUBAZIONE PRIVATA A24'), ('CLT-IRREPERIBILE', 'CLT IRREPERIBILE'), ('RINUNCIA', 'RINUNCIA'), ('GENERICO', 'ECC. DISTANZA / GENERICO')], max_length=256, null=True, verbose_name='Motivo KO')),
                ('msan', models.CharField(blank=True, max_length=256, null=True, verbose_name='Msan')),
                ('rete_rigida', models.CharField(blank=True, choices=[('SI', 'SI'), ('NO', 'NO')], max_length=256, null=True, verbose_name='Rete rigida')),
                ('cavo_cp_cavo', models.CharField(blank=True, max_length=256, null=True, verbose_name='Cavo')),
                ('colonna', models.CharField(blank=True, max_length=256, null=True, verbose_name='Colonna')),
                ('cp_col', models.CharField(blank=True, max_length=256, null=True, verbose_name='Coppia colonna')),
                ('rl', models.CharField(blank=True, max_length=256, null=True, verbose_name='Rl')),
                ('cp_rl', models.CharField(blank=True, max_length=256, null=True, verbose_name='Cp rl')),
                ('secondaria', models.CharField(blank=True, max_length=256, null=True, verbose_name='Secondaria')),
                ('derivato', models.IntegerField(blank=True, default=0, null=True, verbose_name='Derivato')),
                ('presa', models.CharField(blank=True, max_length=256, null=True, verbose_name='Presa')),
                ('cavetto', models.CharField(blank=True, choices=[('TRECCIOLA NUOVA', 'TRECCIOLA NUOVA'), ('TRECCIOLA ESISTENTE', 'TRECCIOLA ESISTENTE'), ('POLITENE NUOVA', 'POLITENE NUOVA'), ('POLITENE ESISTENTE', 'POLITENE ESISTENTE'), ('DROP NUOVA', 'DROP NUOVA'), ('DROP ESISTENTE', 'DROP ESISTENTE')], max_length=256, null=True, verbose_name='Cavetto')),
                ('stato_cavo', models.CharField(blank=True, choices=[('NUOVA POSA', 'NUOVA POSA'), ('ESISTENTE', 'ESISTENTE')], max_length=256, null=True, verbose_name='Stato cavo')),
                ('porta', models.CharField(blank=True, max_length=256, null=True, verbose_name='Porta')),
                ('occorrenze', models.IntegerField(blank=True, default=1, null=True)),
                ('pdf_wr', models.FileField(blank=True, null=True, upload_to='mvm_wr_pdf')),
                ('assigned_to', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mvm import',
                'verbose_name_plural': 'Mvm imports',
            },
        ),
        migrations.CreateModel(
            name='MvmJob',
            fields=[
                ('job_type', models.CharField(max_length=256, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Mvm job type',
                'verbose_name_plural': 'Mvm job types',
            },
        ),
        migrations.CreateModel(
            name='SielteActivity',
            fields=[
                ('servizio', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('guadagno', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
            options={
                'verbose_name': 'Sielte activity',
                'verbose_name_plural': 'Sielte activity',
            },
        ),
        migrations.CreateModel(
            name='SielteExtraActivity',
            fields=[
                ('servizio', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('guadagno', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
            ],
            options={
                'verbose_name': 'Sielte Extra activity',
                'verbose_name_plural': 'Sielte Extra activities',
            },
        ),
        migrations.CreateModel(
            name='SielteImport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_wr_committente', models.CharField(blank=True, max_length=256, null=True)),
                ('impianto', models.CharField(blank=True, max_length=256, null=True)),
                ('descrizione_centrale', models.CharField(blank=True, max_length=256, null=True)),
                ('nome', models.CharField(blank=True, max_length=256, null=True)),
                ('indirizzo', models.CharField(blank=True, max_length=256, null=True)),
                ('descrizione_tipologia_pratica', models.CharField(blank=True, choices=[('VF - Business', 'VF - Business'), ('FW - Business', 'FW - Business'), ('FW - Executive', 'FW - Executive'), ('TT', 'TT'), ('VF - Residenziale', 'VF - Residenziale'), ('FW - Braccialetti Elettronici', 'FW - Braccialetti Elettronici'), ('Adsl', 'Adsl'), ('FW - Manutenzioni Consip', 'FW - Manutenzioni Consip'), ('FW - Attivazioni Consip', 'FW - Attivazioni Consip'), ('Fonia', 'Fonia'), ('Progetti Speciali', 'Progetti Speciali')], max_length=256, null=True)),
                ('nome_assistente', models.CharField(blank=True, max_length=256, null=True)),
                ('tecnico_pratica', models.CharField(blank=True, max_length=256, null=True)),
                ('data_inizio_appuntamento', models.DateField(blank=True, max_length=256, null=True)),
                ('ora_inizio_appuntamento', models.TimeField(blank=True, max_length=256, null=True)),
                ('descrizione_pratica', models.CharField(blank=True, max_length=256, null=True)),
                ('nr', models.CharField(blank=True, max_length=256, null=True)),
                ('cod_stato', models.CharField(blank=True, max_length=256, null=True)),
                ('nome_stato', models.CharField(blank=True, choices=[('New', 'New'), ('Nuovo', 'Nuovo'), ('Sospensione', 'Sospensione'), ('Working', 'Working'), ('Nuova', 'Nuova'), ('TRIAL - Appuntamento', 'TRIAL - Appuntamento'), ('In Lavorazione', 'In Lavorazione'), ('Da Lavorare', 'Da Lavorare'), ('TRIAL - Lavorabile', 'TRIAL - Lavorabile'), ('Programmata', 'Programmata'), ('Sospesa', 'Sospesa'), ('TRIAL - Sospeso', 'TRIAL - Sospeso')], max_length=256, null=True)),
                ('tempo_di_esecuzione', models.IntegerField(blank=True, null=True)),
                ('cod_centrale', models.CharField(blank=True, max_length=256, null=True)),
                ('codice_progetto', models.CharField(blank=True, max_length=256, null=True)),
                ('citta', models.CharField(blank=True, max_length=256, null=True)),
                ('provincia', models.CharField(blank=True, max_length=256, null=True)),
                ('data_di_ricezione', models.DateTimeField(blank=True, max_length=256, null=True)),
                ('aging', models.CharField(blank=True, max_length=256, null=True)),
                ('data_scadenza', models.DateField(blank=True, max_length=256, null=True)),
                ('data_appuntamento_a', models.DateField(blank=True, max_length=256, null=True)),
                ('ora_fine_appuntamento', models.TimeField(blank=True, max_length=256, null=True)),
                ('inizio_lavorazione_prevista', models.DateTimeField(blank=True, max_length=256, null=True)),
                ('fine_lavorazione_prevista', models.DateTimeField(blank=True, max_length=256, null=True)),
                ('data_chiusura', models.DateField(blank=True, max_length=256, null=True)),
                ('ora_chiusura', models.TimeField(blank=True, max_length=256, null=True)),
                ('telefono_cliente_1', models.CharField(blank=True, max_length=256, null=True)),
                ('telefono_cliente_2', models.CharField(blank=True, max_length=256, null=True)),
                ('riferimento_cliente', models.CharField(blank=True, max_length=256, null=True)),
                ('nr_occorrenze', models.IntegerField(blank=True, null=True)),
                ('e_mail', models.CharField(blank=True, max_length=256, null=True)),
                ('identificativo_cliente', models.CharField(blank=True, max_length=256, null=True)),
                ('nome_ubicazione', models.CharField(blank=True, max_length=256, null=True)),
                ('pratica_chiusa', models.BooleanField(default=False)),
                ('pratica_interna', models.BooleanField(default=False)),
                ('pratica_nuova', models.BooleanField(default=False)),
                ('tipo_cliente', models.CharField(blank=True, choices=[('Business', 'Business'), ('Residenziale', 'Residenziale')], max_length=256, null=True)),
                ('tipo_telefono_1', models.CharField(blank=True, max_length=256, null=True)),
                ('tipo_telefono_2', models.CharField(blank=True, max_length=256, null=True)),
                ('note', models.TextField(blank=True, max_length=2048, null=True)),
                ('status', models.CharField(blank=True, choices=[('OK', 'OK'), ('KO', 'KO'), ('SOSPESO', 'SOSPESO'), ('ANNULLATO', 'ANNULLATO')], max_length=256, null=True, verbose_name='Stato lavoro')),
                ('ko_reason', models.CharField(blank=True, choices=[('TUBAZIONE-A14', 'TUBAZIONE PRIVATA A14'), ('TUBAZIONE-A24', 'TUBAZIONE PRIVATA A24'), ('CLT-IRREPERIBILE', 'CLT IRREPERIBILE'), ('RINUNCIA', 'RINUNCIA'), ('GENERICO', 'ECC. DISTANZA / GENERICO')], max_length=256, null=True, verbose_name='Motivo KO')),
                ('ora_da', models.TimeField(blank=True, max_length=256, null=True)),
                ('ora_a', models.TimeField(blank=True, max_length=256, null=True)),
                ('numero_agg', models.IntegerField(blank=True, default=1, null=True)),
                ('occorrenze', models.IntegerField(blank=True, default=1, null=True)),
                ('assigned_to', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
                ('attivita', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='tickets.sielteactivity')),
                ('attivita_aggiuntiva', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='tickets.sielteextraactivity')),
            ],
            options={
                'verbose_name': 'Sielte import',
                'verbose_name_plural': 'Sielte imports',
            },
        ),
        migrations.CreateModel(
            name='UploadedFileSielte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('file', models.FileField(upload_to='file_uploads_sielte')),
                ('obj', models.ForeignKey(default='OBJ_MISSING', on_delete=django.db.models.deletion.SET_DEFAULT, to='tickets.sielteimport')),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFileMvm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('file', models.FileField(upload_to='file_uploads_mvm')),
                ('obj', models.ForeignKey(default='OBJ_MISSING', on_delete=django.db.models.deletion.SET_DEFAULT, to='tickets.mvmimport')),
            ],
        ),
        migrations.AddField(
            model_name='mvmimport',
            name='job_type',
            field=models.ForeignKey(blank=True, default='JOB_MISSING', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='tickets.mvmjob'),
        ),
        migrations.CreateModel(
            name='MvmPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desccent', models.CharField(max_length=256)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('job_type', models.ForeignKey(default='JOB_MISSING', on_delete=django.db.models.deletion.SET_DEFAULT, to='tickets.mvmjob')),
            ],
            options={
                'verbose_name': 'Mvm price',
                'verbose_name_plural': 'Mvm prices',
                'unique_together': {('job_type', 'desccent')},
            },
        ),
    ]
