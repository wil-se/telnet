# Generated by Django 3.2.2 on 2021-06-18 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_auto_20210617_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='plain_text',
            field=models.TextField(blank=True, max_length=2048, null=True),
        ),
    ]