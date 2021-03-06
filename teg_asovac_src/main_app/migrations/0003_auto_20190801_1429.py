# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-08-01 14:29
from __future__ import unicode_literals

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20190619_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='sistema_asovac',
            name='autoridad1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='sistema_asovac',
            name='autoridad2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='sistema_asovac',
            name='firma1',
            field=models.ImageField(blank=True, upload_to=main_app.models.upload_to),
        ),
        migrations.AddField(
            model_name='sistema_asovac',
            name='firma2',
            field=models.ImageField(blank=True, upload_to=main_app.models.upload_to),
        ),
        migrations.AddField(
            model_name='sistema_asovac',
            name='logo',
            field=models.ImageField(default='default/AsoVac_Logo.jpg', upload_to=main_app.models.upload_to),
        ),
    ]
