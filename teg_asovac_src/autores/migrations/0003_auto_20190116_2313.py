# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-01-16 23:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autores', '0002_auto_20190116_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autor',
            name='constancia_estudio',
            field=models.FileField(blank=True, upload_to='constancias_de_estudio/'),
        ),
    ]