# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


"""""""""""""""""""""""""""
Trabajo Model
"""""""""""""""""""""""""""
class Trabajo(models.Model):

	# autor_id = models.ManyToManyField('autores.Autor',through='Autores_trabajos')
	autor_id = models.ManyToManyField('autores.Autor')
	arbitro_id = models.ManyToManyField('arbitrajes.Arbitro',blank=True)

	titulo_espanol = models.CharField(max_length=40)
	titulo_ingles = models.CharField(max_length=40)
	palabras_clave = models.CharField(max_length=40)
	forma_presentacion = models.CharField(max_length=40)
	area = models.CharField(max_length=20)
	subarea1 = models.CharField(max_length=20)
	subarea2 = models.CharField(max_length=20)
	subarea3 = models.CharField(max_length=20)
	resumen = models.TextField(max_length=255,default='')
	documento_inscrito=  models.CharField(max_length=100,blank=True)
	observaciones = models.TextField(max_length=255, blank = True)
	url_trabajo = models.CharField(max_length=255,blank=True)
	version= models.CharField(max_length=20,blank=True)

	def __str__(self):
    		return self.titulo_espanol#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Detalle_version_final Model
"""""""""""""""""""""""""""
class Detalle_version_final(models.Model):
	
	arbitraje_id = models.OneToOneField('arbitrajes.Arbitraje')
	trabajo_id = models.OneToOneField(Trabajo, on_delete = models.CASCADE)

	estatus = models.CharField(max_length=20)
	observaciones = models.TextField(max_length=255, blank = True)
	se_recibio_version_final_corregida = models.BooleanField(default=False)
	url_version_final_trabajo = models.CharField(max_length=35)
	fecha_envio_version_final = models.DateTimeField()
	se_recibio_version_final_presentacion = models.BooleanField(default=False)
	url_version_final_presentacion = models.CharField(max_length=35)
	fecha_envio_version_final_presentacion = models.DateTimeField()
	def __str__(self):
		return self.url_version_final_trabajo#.encode('utf-8', errors='replace')
