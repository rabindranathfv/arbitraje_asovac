# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-30 01:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizador',
            name='genero',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='organizador',
            name='usuario_asovac',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Usuario_asovac'),
        ),
    ]