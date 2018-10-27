# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-16 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='organizador_id',
            field=models.ManyToManyField(related_name='Organizador_eventos', through='eventos.Organizador_evento', to='eventos.Organizador'),
        ),
    ]