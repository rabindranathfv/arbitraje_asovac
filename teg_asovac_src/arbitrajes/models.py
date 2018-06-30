# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


"""""""""""""""""""""""""""
Arbitraje Model
"""""""""""""""""""""""""""
class Arbitraje(models.Model):

	marca_temporal = models.DateTimeField()
	correcciones = models.TextField(max_length=100, blank = True)
	resultado_del_arbitraje = models.TextField(max_length=50, blank = True)
	razones_rechazo = models.TextField(max_length=100, blank = True)
	observaciones = models.TextField(max_length=100, blank = True)
	estatus = models.SmallIntegerField(default=0)
	
	def __str__(self):
		return self.correcciones#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Area Model
"""""""""""""""""""""""""""
class Area(models.Model):
	
	nombre = models.CharField(max_length=20)
	descripcion = models.TextField(max_length=100, blank = True)
	
	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Sub_area Model
"""""""""""""""""""""""""""
class Sub_area(models.Model):
	
	area_id = models.ForeignKey(Area, on_delete = models.CASCADE)

	nombre = models.CharField(max_length=20)
	descripcion = models.TextField(max_length=100, blank = True)

	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Arbitro Model
"""""""""""""""""""""""""""
class Arbitro(models.Model):

	usuario_id = models.OneToOneField('main_app.Usuario_asovac',on_delete = models.CASCADE)
	arbitraje_id = models.ManyToManyField(Arbitraje)
	subarea_id = models.ManyToManyField(Sub_area)

	nombres = models.CharField(max_length=40)
	apellidos = models.CharField(max_length=40)
	cedula_pasaporte = models.CharField(max_length=20)
	titulo = models.CharField(max_length=50)
	correo_electronico = models.EmailField(max_length=254)
	linea_investigacion = models.CharField(max_length=50)
	telefono_oficina = models.CharField(max_length=20)
	telefono_habitacion_celular = models.CharField(max_length=20)
	institucion_trabajo = models.CharField(max_length=50)
	datos_institucion = models.CharField(max_length=100)
	areas_interes = models.CharField(max_length=50)
	observaciones = models.TextField(max_length=100, blank = True)
	clave_arbitro = models.CharField(max_length=100)

	def __str__(self):
		return self.nombres#.encode('utf-8', errors='replace')
