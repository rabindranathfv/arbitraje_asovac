# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

"""""""""""""""""""""""""""
Espacio_fisico Model
"""""""""""""""""""""""""""
class Espacio_fisico(models.Model):
	
	nombre = models.CharField(max_length=20)
	capacidad = models.IntegerField()
	ubicacion = models.TextField(max_length=100, blank = True)
	video_beam = models.BooleanField(default=False)
	portatil = models.BooleanField(default=False)
	turno = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Espacio_virtual Model
"""""""""""""""""""""""""""
class Espacio_virtual(models.Model):
	
	url_virtual = models.CharField(max_length=100)
	capacidad_url = models.IntegerField()
	turno = models.CharField(max_length=50)

	def __str__(self):
		return self.url_virtual#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Espacio Model
"""""""""""""""""""""""""""
class Espacio(models.Model):

	espacio_fisico_id = models.OneToOneField(Espacio_fisico)
	espacio_virtual_id = models.OneToOneField(Espacio_virtual)

	fecha_ocupacion = models.DateTimeField()
	tipo_espacio = models.CharField(max_length=50)

	def __str__(self):
		return self.tipo_espacio#.encode('utf-8', errors='replace')




"""""""""""""""""""""""""""
Sesion Model
"""""""""""""""""""""""""""
class Sesion(models.Model):
	
	arbitraje_id = models.ForeignKey('arbitrajes.Arbitraje')
	espacio_id = models.OneToOneField('sesiones.Espacio')

	Sesion = models.CharField(max_length=15)
	fecha_sesion = models.DateTimeField()
	coordinadores = models.CharField(max_length=100)
	nombre_sesion = models.CharField(max_length=50)
	modalidad = models.CharField(max_length=50)
	observaciones = models.TextField(max_length=100, blank = True)
	fecha_presentacion = models.DateTimeField()

	def __str__(self):
		return self.Sesion#.encode('utf-8', errors='replace')



