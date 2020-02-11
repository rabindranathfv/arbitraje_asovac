# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from eventos.validators import validate_ced_passport,validate_phone_office,validate_phone_personal,validate_cap_asovac 
from django.core.validators import EmailValidator,URLValidator

# Create your models here.

CHOICES_GENERO = (   (0,'Masculino'),
                        (1,'Femenino'),
                        )

CHOICES_MIEMBRO_ASOVAC = (   (False,'No es miembro de AsoVAC'),
                        (True,'Es miembro de AsoVAC'),
                        )

CHOICES_CATEGORIA_EVENTO = (	('P', 'Presencial'),
								('V', 'Virtual'),
	)
"""""""""""""""""""""""""""
Organizador Model
"""""""""""""""""""""""""""
class Organizador(models.Model):

	usuario_asovac = models.ForeignKey('main_app.Usuario_asovac',related_name='Usuarios_asovac_organizadores')

	nombres = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	genero = models.SmallIntegerField(default=0,choices=CHOICES_GENERO)
	cedula_o_pasaporte = models.CharField(max_length=20)
    #Formato de ejemplo para agregar validators
    #correo_electronico = models.EmailField(max_length=254,validators=[EmailValidator()])
	correo_electronico = models.EmailField(max_length=254)
	institucion = models.CharField(max_length=50)
	telefono_oficina = models.CharField(max_length=20)
	telefono_habitacion_celular = models.CharField(max_length=20)
	direccion_correspondencia = models.TextField(max_length=100)
	es_miembro_asovac = models.BooleanField(default=False,choices=CHOICES_MIEMBRO_ASOVAC)
	capitulo_asovac = models.CharField(max_length=50)
	cargo_en_institucion = models.CharField(max_length=50)
	url_organizador = models.CharField(max_length=200)
	observaciones = models.TextField(max_length=400, blank=True)

	def __str__(self):
		return "{}".format(self.correo_electronico)#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Locacion_evento Model
"""""""""""""""""""""""""""
#Quitar _ del nombre del modelo
class Locacion_evento(models.Model):

	lugar = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=255)
	capacidad_de_asistentes = models.SmallIntegerField(default=0)
	observaciones = models.TextField(max_length=400, blank=True)
	equipo_requerido = models.CharField(max_length=255)
	
	def __str__(self):
		return self.lugar#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Evento Model
"""""""""""""""""""""""""""
class Evento(models.Model):

	organizador_id = models.ManyToManyField(Organizador, through ='Organizador_evento',related_name='Organizador_eventos')
	locacion_evento = models.ForeignKey(Locacion_evento,related_name='locacion_eventos')
	sistema_asovac = models.ForeignKey('main_app.Sistema_asovac')

	nombre = models.CharField(max_length=150)
	categoria = models.CharField(max_length=50, choices = CHOICES_CATEGORIA_EVENTO)
	descripcion = models.TextField(max_length=150)
	tipo = models.CharField(max_length=50)
	fecha_inicio = models.DateField()
	fecha_fin = models.DateField()
	hora_inicio = models.TimeField()
	hora_fin = models.TimeField()
	imagen = models.ImageField(blank=True,upload_to='eventos/')
	dia_asignado = models.DateField()
	duracion = models.CharField(max_length=50)
	horario_preferido = models.CharField(max_length=50)
	# OJO antes era TimeField
	fecha_preferida = models.DateField()
	observaciones = models.TextField(max_length=400, blank = True)
    #Agregar blank=True
	url_anuncio_evento = models.CharField(blank=True,max_length=200,validators=[URLValidator()])

	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Organizador_evento Model
"""""""""""""""""""""""""""
#Quitar _ del nombre del modelo

class Organizador_evento(models.Model):

	evento = models.ForeignKey(Evento,related_name='Eventos',on_delete=models.CASCADE)
	organizador = models.ForeignKey(Organizador,related_name='Organizadores')

	locacion_preferida = models.CharField(max_length=50)

	def __str__(self):
		return self.locacion_preferida#.encode('utf-8', errors='replace')






