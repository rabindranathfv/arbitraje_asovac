# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-28 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('autores', '0001_initial'),
        ('main_app', '0001_initial'),
        ('trabajos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='autores_trabajos',
            name='trabajo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trabajos.Trabajo'),
        ),
        migrations.AddField(
            model_name='autor',
            name='universidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autores.Universidad'),
        ),
        migrations.AddField(
            model_name='autor',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.Usuario_asovac'),
        ),
    ]
