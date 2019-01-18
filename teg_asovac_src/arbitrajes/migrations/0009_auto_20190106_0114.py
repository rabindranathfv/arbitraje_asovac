# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-06 01:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arbitrajes', '0008_auto_20190102_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arbitro',
            name='areas_interes',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='arbitro',
            name='correo_electronico',
            field=models.EmailField(max_length=150),
        ),
        migrations.AlterField(
            model_name='arbitro',
            name='datos_institucion',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='arbitro',
            name='genero',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='arbitro',
            name='institucion_trabajo',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='arbitro',
            name='linea_investigacion',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='arbitro',
            name='observaciones',
            field=models.TextField(blank=True, max_length=254),
        ),
    ]