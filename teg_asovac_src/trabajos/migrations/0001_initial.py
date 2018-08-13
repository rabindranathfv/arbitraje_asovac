# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-12 14:03
from __future__ import unicode_literals

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
                ('estatus', models.CharField(max_length=20)),
                ('observaciones', models.TextField(blank=True, max_length=255)),
                ('se_recibio_version_final_corregida', models.BooleanField(default=False)),
                ('url_version_final_trabajo', models.CharField(blank=True, max_length=35)),
                ('fecha_envio_version_final', models.DateField()),
                ('se_recibio_version_final_presentacion', models.BooleanField(default=False)),
                ('url_version_final_presentacion', models.CharField(max_length=35)),
                ('fecha_envio_version_final_presentacion', models.DateField()),
                ('arbitraje', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='arbitrajes.Arbitraje')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo_espanol', models.CharField(max_length=40)),
                ('titulo_ingles', models.CharField(blank=True, max_length=40)),
                ('palabras_clave', models.CharField(blank=True, max_length=40)),
                ('forma_presentacion', models.CharField(max_length=40)),
                ('area', models.CharField(max_length=20)),
                ('subarea1', models.CharField(max_length=20)),
                ('subarea2', models.CharField(blank=True, max_length=20)),
                ('subarea3', models.CharField(blank=True, max_length=20)),
                ('resumen', models.TextField(max_length=255)),
                ('documento_inscrito', models.CharField(blank=True, max_length=100)),
                ('observaciones', models.TextField(blank=True, max_length=255)),
                ('url_trabajo', models.CharField(blank=True, max_length=255)),
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
