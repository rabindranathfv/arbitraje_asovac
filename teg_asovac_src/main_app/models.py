# -*- coding: utf-8 necessary for django string usage -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid
# Create your models here.

# Este es un diccionario con los estados numericos y en string de los arbitrajes.
estados_arbitraje = {	'0':'Desactivado',
						'1':'Iniciado',
						'2':'En Selección y Asignación de Coordinadores de Área',
						'3':'En Carga de Trabajos',
						'4':'En Asignación de Trabajos a las Áreas',
						'5':'En Arbitraje',
						'6':'En Cierre de Arbitraje',
						'7':'En Asignación de Secciones',
						'8':'En Resumen'}

"""""""""""""""""""""""""""
Rol Model
"""""""""""""""""""""""""""
class Rol(models.Model):

	nombre = models.CharField(max_length=80)
	descripcion = models.TextField(max_length=255)
	
	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Area Model
"""""""""""""""""""""""""""
class Area(models.Model):

	nombre = models.CharField(max_length=80)
	descripcion = models.TextField(max_length=150, blank = True)
	
	def __str__(self):
		return self.nombre.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Sub_area Model
"""""""""""""""""""""""""""
class Sub_area(models.Model):

	area = models.ForeignKey(Area, on_delete = models.CASCADE)

	nombre = models.CharField(max_length=80)
	descripcion = models.TextField(max_length=150, blank = True)

	def __str__(self):
		return self.nombre.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Sistema_asovac Model
"""""""""""""""""""""""""""
class Sistema_asovac(models.Model):

	nombre = models.CharField(max_length=80)
	descripcion = models.TextField(max_length=255)
	fecha_inicio_arbitraje = models.DateField()
	fecha_fin_arbitraje = models.DateField()
	coordinador_general = models.ForeignKey('Usuario_asovac',blank = True, null = True)
	estado_arbitraje = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(8)])
	clave_maestra_coordinador_area = models.CharField(max_length=100,blank=True)
	clave_maestra_arbitro_area = models.CharField(max_length=100,blank=True)
	clave_maestra_coordinador_general = models.CharField(max_length=100,blank=True)
	clave_maestra_arbitro_subarea = models.CharField(max_length=100,blank=True)
	
	def __str__(self):
		return self.nombre#.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Usuario_asovac Model
"""""""""""""""""""""""""""
class Usuario_asovac(models.Model):

	usuario = models.OneToOneField(User, on_delete = models.CASCADE)
	rol = models.ManyToManyField(Rol,blank=True)
	Sistema_asovac_id = models.ManyToManyField(Sistema_asovac, blank=True)
	sub_area = models.ManyToManyField(Sub_area, blank=True)

	usuario_activo = models.BooleanField(default=True)

	def biggest_role(self):
		my_roles = self.rol.all()
		biggest_role = None
		for role in my_roles:
			if biggest_role:
				if role.id < biggest_role.id:
					biggest_role = role
			else:
				biggest_role = role
		return biggest_role

	def __str__(self):
		return "{} {}".format(self.usuario.first_name,self.usuario.last_name)#.encode('utf-8', errors='replace')




#Esta seccion de codigo nos permite crear un objeto Usuario_asovac
#Por cada objeto User creado en el sistema automaticamente.
def crear_usuario_asovac(sender, **kwargs):

	user = kwargs["instance"]
	if kwargs["created"]:
		usuario_asovac = Usuario_asovac(usuario=user)
		usuario_asovac.save()

		first_usuario_asovac = Usuario_asovac.objects.count()
		roles = Rol.objects.count()

		if first_usuario_asovac == 1 and roles == 0: #Esto asegura la creación de roles al momento de crear el primer usuario
			rol = Rol(nombre="Admin", descripcion="Administrador")
			rol.save()

			rol = Rol(nombre="Coordinador General", descripcion ="CG")
			rol.save()

			rol = Rol(nombre="Coordinador de Area", descripcion ="CA")
			rol.save()

			rol = Rol(nombre="Arbitro de Subarea", descripcion ="AS")
			rol.save()

			rol = Rol(nombre="Autor",descripcion="Autor")
			rol.save()


		usuario_asovac.rol.add(Rol.objects.get(id=5)) #Los roles se crean en base a la tabla de roles, autor es id=5
		usuario_asovac.save()

post_save.connect(crear_usuario_asovac, sender=User)



