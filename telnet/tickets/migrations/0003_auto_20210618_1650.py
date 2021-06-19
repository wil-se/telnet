# Generated by Django 3.2.2 on 2021-06-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_sielteimport_tot_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sielteimport',
            name='aging',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='citta',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='cod_centrale',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='cod_stato',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='cod_wr_committente',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='codice_progetto',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='descrizione_centrale',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='descrizione_pratica',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='descrizione_tipologia_pratica',
            field=models.CharField(blank=True, choices=[('VF - Business', 'VF - Business'), ('FW - Business', 'FW - Business'), ('FW - Executive', 'FW - Executive'), ('TT', 'TT'), ('VF - Residenziale', 'VF - Residenziale'), ('FW - Braccialetti Elettronici', 'FW - Braccialetti Elettronici'), ('Adsl', 'Adsl'), ('FW - Manutenzioni Consip', 'FW - Manutenzioni Consip'), ('FW - Attivazioni Consip', 'FW - Attivazioni Consip'), ('Fonia', 'Fonia'), ('Progetti Speciali', 'Progetti Speciali')], default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='e_mail',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='identificativo_cliente',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='impianto',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='indirizzo',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='nome_assistente',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='nome_stato',
            field=models.CharField(blank=True, choices=[('New', 'New'), ('Nuovo', 'Nuovo'), ('Sospensione', 'Sospensione'), ('Working', 'Working'), ('Nuova', 'Nuova'), ('TRIAL - Appuntamento', 'TRIAL - Appuntamento'), ('In Lavorazione', 'In Lavorazione'), ('Da Lavorare', 'Da Lavorare'), ('TRIAL - Lavorabile', 'TRIAL - Lavorabile'), ('Programmata', 'Programmata'), ('Sospesa', 'Sospesa'), ('TRIAL - Sospeso', 'TRIAL - Sospeso')], default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='nome_ubicazione',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='nr',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='provincia',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='riferimento_cliente',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='tecnico_pratica',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='telefono_cliente_1',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='telefono_cliente_2',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='tipo_cliente',
            field=models.CharField(blank=True, choices=[('Business', 'Business'), ('Residenziale', 'Residenziale')], default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='tipo_telefono_1',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='sielteimport',
            name='tipo_telefono_2',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]