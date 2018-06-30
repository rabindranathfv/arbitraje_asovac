# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

"""""""""""""""""""""""""""
Universidad Model
"""""""""""""""""""""""""""
class Universidad(models.Model):
	
	nombre = models.CharField(max_length=100)
	facultad = models.CharField(max_length=100)
	escuela = models.CharField(max_length=100)
	instituto_investigacion = models.CharField(max_length=100)
	
	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Autor Model
"""""""""""""""""""""""""""
class Autor(models.Model):

	usuario_id = models.OneToOneField('main_app.Usuario_asovac',on_delete = models.CASCADE)
	universidad_id = models.ForeignKey(Universidad)

	marca_temporal = models.DateTimeField(auto_now=True)
	nombres = models.CharField(max_length=40)
	apellidos = models.CharField(max_length=40)
	genero = models.CharField(max_length=1)
	cedula_pasaporte = models.CharField(max_length=20)
	correo_electronico = models.EmailField(max_length=254)
	telefono_oficina = models.CharField(max_length=20)
	telefono_habitacion_celular= models.CharField(max_length=20)
	# Constancia de estudio no se sabe qué será
	direccion_envio_correspondencia = models.TextField(max_length=100,blank=True)
	es_miembro_asovac = models.BooleanField(default=False)
	capitulo_perteneciente = models.CharField(max_length=20,blank=True)
	nivel_intruccion = models.CharField(max_length=50)
	observaciones = models.TextField(max_length=255, blank = True)
	
	def __str__(self):
		return self.nombres#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Autores_trabajos Model - Es la tabla intermedia entre Trabajo, Autor y Pagador
"""""""""""""""""""""""""""
class Autores_trabajos(models.Model):
	
	autor_id = models.ForeignKey(Autor, on_delete = models.CASCADE)
	trabajo_id = models.ForeignKey('trabajos.Trabajo', on_delete = models.CASCADE)

	es_autor_principal = models.BooleanField(default=False)
	es_ponente = models.BooleanField(default=False)
	es_coautor = models.BooleanField(default=False)
	monto_total = models.FloatField()
	pagado = models.BooleanField(default=False)

	def __str__(self):

		return "{} autor trabajo".format(self.autor_id.nombres)#.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Datos_pagador Model
"""""""""""""""""""""""""""
class Datos_pagador(models.Model):
	
	cedula = models.CharField(max_length=10) 
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	pasaporte_rif = models.CharField(max_length=20)
	telefono_oficina = models.CharField(max_length=20)
	telefono_habitacion_celular = models.CharField(max_length=20)
	direccion_fiscal = models.TextField(max_length=100)
	def __str__(self):
		return self.cedula#.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Pagador Model
"""""""""""""""""""""""""""
class Pagador(models.Model):
	
	autor_trabajo = models.ForeignKey(Autores_trabajos,blank=True, null=True)
	datos_pagador = models.OneToOneField(Datos_pagador)

	categorias_pago = models.CharField(max_length=20)

	def __str__(self):
		return self.categorias_pago#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Pago Model
"""""""""""""""""""""""""""
class Pago(models.Model):

	tipo_pago = models.CharField(max_length=50)
	numero_cuenta_origen = models.CharField(max_length=50)
	banco_origen = models.CharField(max_length=50)
	numero_transferencia = models.CharField(max_length=50)
	numero_cheque = models.CharField(max_length=50)
	fecha_pago = models.DateTimeField()
	observaciones = models.TextField(max_length=100,blank=True)
	comprobante_pago = models.TextField(max_length=100)

	def __str__(self):
		return self.numero_transferencia#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Factura Model
"""""""""""""""""""""""""""
class Factura(models.Model):

	pagador = models.ForeignKey(Pagador)
	pago = models.OneToOneField(Pago)

	monto_subtotal = models.FloatField()
	fecha_emision = models.DateTimeField()
	monto_total = models.FloatField()
	iva = models.FloatField()
	def __str__(self):
		return self.monto_subtotal#.encode('utf-8', errors='replace')


