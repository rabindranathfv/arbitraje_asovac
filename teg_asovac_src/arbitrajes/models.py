# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from main_app.models import Sistema_asovac,Usuario_asovac

# Create your models here.


"""""""""""""""""""""""""""
Arbitraje Model
"""""""""""""""""""""""""""
class Arbitraje(models.Model):

	marca_temporal = models.DateTimeField(auto_now=True)
	correcciones = models.TextField(max_length=100, blank = True)
	resultado_del_arbitraje = models.TextField(max_length=50, blank = True)
	razones_rechazo = models.TextField(max_length=100, blank = True)
	observaciones = models.TextField(max_length=100, blank = True)
	estatus = models.SmallIntegerField(default=0)
	
	def __str__(self):
		return self.correcciones#.encode('utf-8', errors='replace')



# """""""""""""""""""""""""""
# Area Model
# """""""""""""""""""""""""""
# class Area(models.Model):
	
# 	nombre = models.CharField(max_length=20)
# 	descripcion = models.TextField(max_length=100, blank = True)
	
# 	def __str__(self):
# 		return self.nombre#.encode('utf-8', errors='replace')


# """""""""""""""""""""""""""
# Sub_area Model
# """""""""""""""""""""""""""
# class Sub_area(models.Model):
	
# 	area_id = models.ForeignKey(Area, on_delete = models.CASCADE)

# 	nombre = models.CharField(max_length=20)
# 	descripcion = models.TextField(max_length=100, blank = True)

# 	def __str__(self):
# 		return self.nombre#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Arbitro Model
"""""""""""""""""""""""""""
class Arbitro(models.Model):

	usuario = models.OneToOneField('main_app.Usuario_asovac',on_delete = models.CASCADE,blank=True, null=True)
	arbitraje = models.ManyToManyField(Arbitraje,blank=True)
	Sistema_asovac = models.ManyToManyField('main_app.Sistema_asovac', blank=True)

	nombres = models.CharField(max_length=40)
	apellidos = models.CharField(max_length=40)
	genero = models.CharField(max_length=5)
	cedula_pasaporte = models.CharField(max_length=20)
	titulo = models.CharField(max_length=50)
	correo_electronico = models.EmailField(max_length=254)
	linea_investigacion = models.CharField(max_length=50)
	telefono_oficina = models.CharField(max_length=20,blank=True)
	telefono_habitacion_celular = models.CharField(max_length=20)
	institucion_trabajo = models.CharField(max_length=50,blank=True)
	datos_institucion = models.CharField(max_length=100,blank=True)
	areas_interes = models.CharField(max_length=50,blank=True)
	observaciones = models.TextField(max_length=100, blank = True)
	clave_arbitro = models.CharField(max_length=100,blank=True)

	def __str__(self):
		return self.nombres#.encode('utf-8', errors='replace')

# """""""""""""""""""""""""""
# arbitrajes_arbitro_Sistema_asovac_id Model
# """""""""""""""""""""""""""
# class Arbitros_Sistema_asovac(models.Model):
	
# 	arbitro = models.ForeignKey(Arbitro)
# 	sistema_asovac = models.ForeignKey(Sistema_asovac)


# 	def __str__(self):
# 		return "{} {} {}".format(self.arbitro.nombres,self.sistema_asovac.nombre).encode('utf-8', errors='replace')

