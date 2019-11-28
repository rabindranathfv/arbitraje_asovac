# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-11-28 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0002_evento_sistema_asovac'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='hora_fin',
            field=models.TimeField(default='8:00 AM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evento',
            name='hora_inicio',
            field=models.TimeField(default='7:00 AM'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evento',
            name='imagen',
            field=models.ImageField(default='', upload_to='eventos/'),
            preserve_default=False,
        ),
    ]
