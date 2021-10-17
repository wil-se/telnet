# Generated by Django 3.2.2 on 2021-10-17 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0005_alter_sielteimport_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MvmExport',
        ),
        migrations.AlterUniqueTogether(
            name='mvmprice',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='mvmprice',
            name='job_type',
        ),
        migrations.RemoveField(
            model_name='uploadedfilemvm',
            name='obj',
        ),
        migrations.DeleteModel(
            name='MvmImport',
        ),
        migrations.DeleteModel(
            name='MvmJob',
        ),
        migrations.DeleteModel(
            name='MvmPrice',
        ),
        migrations.DeleteModel(
            name='UploadedFileMvm',
        ),
    ]
