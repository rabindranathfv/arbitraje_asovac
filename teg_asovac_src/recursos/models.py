# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Recurso(models.Model):

    usuario_asovac = models.ManyToManyField('main_app.Usuario_asovac')

    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre 

class Resumen (models.Model):

    sistema= models.ForeignKey('main_app.Sistema_asovac',blank=True,null=True)
    url_portada= models.CharField(max_length=200,blank=True,null=True)
    url_patrocinadores= models.CharField(max_length=200,blank=True,null=True)
    comision_organizadora= models.TextField(blank=True,null=True)
    pie_pagina= models.TextField(blank=True,null=True)