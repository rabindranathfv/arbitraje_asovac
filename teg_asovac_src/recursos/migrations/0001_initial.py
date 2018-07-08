# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-04 00:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0004_auto_20180703_0413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200)),
                ('usuario_asovac', models.ManyToManyField(to='main_app.Usuario_asovac')),
            ],
        ),
    ]