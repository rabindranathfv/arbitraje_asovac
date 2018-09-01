# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

choises_genero = (   (0,'Masculino'),
                        (1,'Femenino'),
                        )

choises_mienbro_asovac = (   (False,'No es mienbro de AsoVAC'),
                        (True,'Es mienbro de AsoVAC'),
                        )

"""""""""""""""""""""""""""
Organizador Model
"""""""""""""""""""""""""""
class Organizador(models.Model):

	usuario_asovac = models.ForeignKey('main_app.Usuario_asovac')

	nombres = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	genero = models.SmallIntegerField(default=0,choices=choises_genero)
	cedula_o_pasaporte = models.CharField(max_length=20)
	correo_electronico = models.EmailField(max_length=254)
	institucion = models.CharField(max_length=50)
	telefono_oficina = models.CharField(max_length=20)
	telefono_habitacion_celular = models.CharField(max_length=20)
	direccion_correspondencia = models.TextField(max_length=100)
	es_miembro_asovac = models.BooleanField(default=False,choices=choises_mienbro_asovac)
	capitulo_asovac = models.CharField(max_length=50)
	cargo_en_institucion = models.CharField(max_length=50)
	url_organizador = models.CharField(max_length=100)
	observaciones = models.TextField(max_length=100, blank = True)

	def __str__(self):
		return self.nombres#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Locacion_evento Model
"""""""""""""""""""""""""""
class Locacion_evento(models.Model):

	lugar = models.TextField(max_length=100)
	descripcion = models.TextField(max_length=100)
	capacidad_de_asistentes = models.IntegerField()
	observaciones = models.TextField(max_length=100)
	equipo_requerido = models.TextField(max_length=50)
	
	def __str__(self):
		return self.lugar#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Evento Model
"""""""""""""""""""""""""""
class Evento(models.Model):

	organizador_id = models.ManyToManyField(Organizador, through ='Organizador_evento')
	locacion_evento = models.ForeignKey(Locacion_evento)

	nombre = models.CharField(max_length=50)
	categoria = models.CharField(max_length=50)
	descripcion = models.TextField(max_length=100)
	tipo = models.CharField(max_length=50)
	fecha_inicio = models.DateTimeField()
	fecha_fin = models.DateTimeField()
	dia_asignado = models.DateTimeField()
	duracion = models.CharField(max_length=50)
	horario_preferido = models.CharField(max_length=50)
	fecha_preferida = models.DateTimeField()
	observaciones = models.TextField(max_length=100, blank = True)
	url_anuncio_evento = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Organizador_evento Model
"""""""""""""""""""""""""""
class Organizador_evento(models.Model):

	evento = models.ForeignKey(Evento)
	organizador = models.ForeignKey(Organizador)

	locacion_preferida = models.CharField(max_length=50)

	def __str__(self):
		return self.locacion_preferida#.encode('utf-8', errors='replace')






