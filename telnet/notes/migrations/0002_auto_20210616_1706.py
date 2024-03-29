# Generated by Django 3.2.2 on 2021-06-16 17:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='end_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, max_length=256, null=True),
        ),
    ]
