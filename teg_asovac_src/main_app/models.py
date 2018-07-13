# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
#from .views import cod_generator
import uuid

# Create your models here.


"""""""""""""""""""""""""""
Rol Model
"""""""""""""""""""""""""""
class Rol(models.Model):

	
	nombre = models.CharField(max_length=20)
	descripcion = models.TextField(max_length=255)
	
	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')



"""""""""""""""""""""""""""
Sistema_asovac Model
"""""""""""""""""""""""""""
class Sistema_asovac(models.Model):
	
	nombre = models.CharField(max_length=20)
	descripcion = models.TextField(max_length=255)
	estado_arbitraje = models.SmallIntegerField(default=0)
	fecha_inicio_arbitraje = models.DateTimeField()
	fecha_fin_arbitraje = models.DateTimeField()
	clave_maestra_coordinador_area = models.TextField(max_length=100)
	clave_maestra_arbitro_area = models.TextField(max_length=100)
	clave_maestra_coordinador_general = models.TextField(max_length=100)
	clave_maestra_arbitro_subarea = models.TextField(max_length=100)
	
	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Usuario_asovac Model
"""""""""""""""""""""""""""
class Usuario_asovac(models.Model):

	usuario = models.OneToOneField(User, on_delete = models.CASCADE)
	rol = models.ManyToManyField(Rol)
	Sistema_asovac_id = models.ManyToManyField(Sistema_asovac)

	estado_arbitraje = models.SmallIntegerField(default=0)
	usuario_activo = models.BooleanField(default=True)
	

	def __str__(self):

		return "{} usuario asovac".format(self.usuario_id.get_username())#.encode('utf-8', errors='replace')




#Esta seccion de codigo nos permite crear un objeto Usuario_asovac
#Por cada objeto User creado en el sistema automaticamente.
def crear_usuario_asovac(sender, **kwargs):


	user = kwargs["instance"]
	if kwargs["created"]:
		usuario_asovac = Usuario_asovac(usuario=user)
		usuario_asovac.save()

post_save.connect(crear_usuario_asovac, sender=User)



