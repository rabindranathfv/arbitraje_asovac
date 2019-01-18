# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
CHOICES_GENERO = ((0,'Masculino'),
                 (1,'Femenino'),
                 )

# Create your models here.
CHOICES_CATEGORIA_PAGO = (('P','Personal'),
                 ('I','Institutos profesionales'),
                 ('T', 'Terceros'),
				 ('U', 'Universidades')
                 )

# Create your models here.
CHOICES_TIPO_PAGO = (('T','Transferencia'),
                 ('C','Cheque'),
                 )


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

	usuario = models.OneToOneField('main_app.Usuario_asovac',on_delete = models.CASCADE)
	universidad = models.ForeignKey(Universidad)

	marca_temporal = models.DateTimeField(auto_now=True)
	nombres = models.CharField(max_length=40)
	apellidos = models.CharField(max_length=40)
	genero = models.SmallIntegerField(choices=CHOICES_GENERO)
	cedula_pasaporte = models.CharField(max_length=20)
	correo_electronico = models.EmailField(max_length=254)
	telefono_oficina = models.CharField(max_length=20)
	telefono_habitacion_celular = models.CharField(max_length=20)
	constancia_estudio = models.FileField(upload_to = 'constancias_de_estudio/', blank = True)
	direccion_envio_correspondencia = models.TextField(max_length=100,blank=True)
	es_miembro_asovac = models.BooleanField(default=False)
	capitulo_perteneciente = models.CharField(max_length=20,blank=True)
	nivel_instruccion = models.CharField(max_length=50)
	observaciones = models.TextField(max_length=255, blank = True)
	
	def __str__(self):
		return self.nombres.encode('utf-8', errors='replace')




"""""""""""""""""""""""""""
Autores_trabajos Model - Es la tabla intermedia entre Trabajo, Autor y Pagador
"""""""""""""""""""""""""""
class Autores_trabajos(models.Model):
	
	autor = models.ForeignKey(Autor, on_delete = models.CASCADE)
	trabajo = models.ForeignKey('trabajos.Trabajo', on_delete = models.CASCADE)
	sistema_asovac = models.ForeignKey('main_app.Sistema_asovac')

	es_autor_principal = models.BooleanField(default=False)
	es_ponente = models.BooleanField(default=False)
	es_coautor = models.BooleanField(default=False)
	monto_total = models.FloatField(default = 100) #Falta que se indique el monto total
	pagado = models.BooleanField(default=False)

	def __str__(self):
		return "{} - {}".format(self.autor.nombres, self.trabajo.titulo_espanol)#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Datos_pagador Model
"""""""""""""""""""""""""""
class Datos_pagador(models.Model):
    	
	Sistema_asovac_id = models.ManyToManyField('main_app.Sistema_asovac', blank = True)
	
	cedula = models.CharField(max_length=10) 
	nombres = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	pasaporte_rif = models.CharField(max_length=20, blank = True)
	telefono_oficina = models.CharField(max_length=20, blank = True)
	telefono_habitacion_celular = models.CharField(max_length=20)
	direccion_fiscal = models.TextField(max_length=100)
	categorias_pago = models.CharField(max_length=20, choices = CHOICES_CATEGORIA_PAGO)
	def __str__(self):
		return self.cedula#.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Pagador Model
"""""""""""""""""""""""""""
class Pagador(models.Model):
	
	autor_trabajo = models.ForeignKey(Autores_trabajos,blank=True, null=True)
	datos_pagador = models.OneToOneField(Datos_pagador)


	def __str__(self):
		return self.autor_trabajo.autor.nombres#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Pago Model
"""""""""""""""""""""""""""
CHOICES_BANCO = ( 
					(0,'Banco Caroní'),
                    (1,'Corp Banca'),
                    (2,'Banco del Caribe'),
                    (3,'Bancoro'),
                    (4,'Banco de Venezuela'),
                    (5,'Banco Sofitasa'),
                    (6,'Banpro'),
                    (7,'Banco Provincial'),
                    (8,'Banesco'),
                    (9,'Banco Fondo Común'),
                    (10,'Banfoandes'),
                    (11,'Banco Occidental de Descuento'),
                    (12,'Banco Venezolano de crédito'),
                    (13,'Banco Exterior'),
                    (14,'Banco Industrial de Venezuela'),
                    (15,'Banco Mercantil'),
                    (16,'Banco Plaza'),
                    (17,'Citibank'),
                    (18,'Banco Federal'),
                  )


class Pago(models.Model):


	tipo_pago = models.CharField(max_length=1, choices = CHOICES_TIPO_PAGO)
	numero_cuenta_origen = models.CharField(max_length=50)
	banco_origen = models.SmallIntegerField(choices = CHOICES_BANCO)
	numero_transferencia = models.CharField(max_length=50, blank = True)
	numero_cheque = models.CharField(max_length=50, blank = True)
	fecha_pago = models.DateField()
	observaciones = models.TextField(max_length=100,blank=True)
	comprobante_pago = models.FileField(upload_to = 'comprobantes_de_pago/') # Hacer validacion y path

	def __str__(self):
		return self.numero_cuenta_origen#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Factura Model
"""""""""""""""""""""""""""
class Factura(models.Model):

	pagador = models.ForeignKey(Pagador)
	pago = models.OneToOneField(Pago)

	monto_subtotal = models.FloatField()
	fecha_emision = models.DateField()
	iva = models.FloatField()
	monto_total = models.FloatField()
	
	def __str__(self):
		return self.pago.tipo_pago#.encode('utf-8', errors='replace')
	#def __str__(self):
	 	#return self.fecha_emision#.encode('utf-8', errors='replace')
