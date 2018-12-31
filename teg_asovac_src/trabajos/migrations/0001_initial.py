# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-07 14:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import trabajos.models
import trabajos.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('arbitrajes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle_version_final',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estatus_final', models.CharField(default='Pendiente', max_length=20)),
                ('observaciones', models.TextField(blank=True, max_length=255)),
                ('se_recibio_version_final_corregida', models.BooleanField(default=False)),
                ('fecha_envio_version_final', models.DateField(default=datetime.datetime.now)),
                ('se_recibio_version_final_presentacion', models.BooleanField(default=False)),
                ('url_version_final_presentacion', models.CharField(max_length=35)),
                ('fecha_envio_version_final_presentacion', models.DateField(blank=True, null=True)),
                ('arbitraje', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arbitrajes.Arbitraje')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estatus', models.CharField(default='Pendiente', max_length=20)),
                ('titulo_espanol', models.CharField(max_length=100)),
                ('titulo_ingles', models.CharField(blank=True, max_length=100)),
                ('palabras_clave', models.CharField(blank=True, max_length=60)),
                ('forma_presentacion', models.CharField(max_length=40)),
                ('area', models.CharField(max_length=70)),
                ('subarea1', models.CharField(max_length=70)),
                ('subarea2', models.CharField(blank=True, max_length=70)),
                ('subarea3', models.CharField(blank=True, max_length=70)),
                ('resumen', models.TextField(max_length=255)),
                ('documento_inscrito', models.CharField(blank=True, max_length=100)),
                ('observaciones', models.TextField(blank=True, max_length=255)),
                ('url_trabajo', models.URLField(blank=True, max_length=255)),
                ('version', models.CharField(blank=True, max_length=20)),
                ('archivo_trabajo', models.FileField(upload_to=trabajos.models.job_directory_path, validators=[trabajos.validators.validate_file_extension])),
                ('arbitro_id', models.ManyToManyField(blank=True, to='arbitrajes.Arbitro')),
            ],
        ),
        migrations.AddField(
            model_name='detalle_version_final',
            name='trabajo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='trabajos.Trabajo'),
        ),
    ]
