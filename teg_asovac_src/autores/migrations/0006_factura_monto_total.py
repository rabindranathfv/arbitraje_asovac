# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-08 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autores', '0005_auto_20180908_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='monto_total',
            field=models.FloatField(default=100),
            preserve_default=False,
        ),
    ]
