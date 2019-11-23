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
    url_afiche= models.CharField(max_length=200,blank=True,null=True)
    url_patrocinadores= models.CharField(max_length=200,blank=True,null=True)
    comision_organizadora= models.TextField(blank=True,null=True)
    invitacion= models.TextField(blank=True,null=True)
    cabecera= models.TextField(blank=True,null=True)
    presidente_nombre= models.CharField(max_length=200,blank=True,null=True)
    presidente_cargo= models.CharField(max_length=200,blank=True,null=True)
    presidente_contenido= models.TextField(blank=True,null=True)
    secretario_nombre= models.CharField(max_length=200,blank=True,null=True)
    secretario_cargo= models.CharField(max_length=200,blank=True,null=True)
    secretario_contenido=models.TextField(blank=True,null=True)
    afiche_titulo= models.CharField(max_length=200,blank=True,null=True)
    



