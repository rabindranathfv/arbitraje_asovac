# -*- coding: utf-8 -*-
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
						'7':'En Asignación de Sesiones',
						'8':'En Resumen'}

"""""""""""""""""""""""""""
Rol Model
"""""""""""""""""""""""""""
class Rol(models.Model):

	nombre = models.CharField(max_length=80)
	descripcion = models.TextField(max_length=255)

	def __str__(self):
		return self.nombre.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Area Model
"""""""""""""""""""""""""""
class Area(models.Model):

	nombre = models.CharField(max_length=100)
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
	porcentaje_iva = models.SmallIntegerField()
	monto_pagar_trabajo = models.IntegerField()

	def __str__(self):
		return self.nombre.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Usuario_asovac Model
"""""""""""""""""""""""""""
class Usuario_asovac(models.Model):

	usuario = models.OneToOneField(User, on_delete = models.CASCADE)
	sub_area = models.ManyToManyField(Sub_area, blank=True)

	usuario_activo = models.BooleanField(default=True)

	def __str__(self):
		return "{} {}".format(self.usuario.first_name,self.usuario.last_name).encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Usuario_rol_in_sistema Model
"""""""""""""""""""""""""""
class Usuario_rol_in_sistema(models.Model):

	rol = models.ForeignKey(Rol)
	sistema_asovac = models.ForeignKey(Sistema_asovac,blank=True,null=True)
	usuario_asovac = models.ForeignKey(Usuario_asovac)

	status = models.BooleanField(default = True)

	def __str__(self):
		return "{} {} {}".format(self.usuario_asovac.usuario.first_name,self.usuario_asovac.usuario.last_name,self.rol.descripcion).encode('utf-8', errors='replace')

"""
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
"""







#Esta seccion de codigo nos permite crear un objeto Usuario_asovac
#Por cada objeto User creado en el sistema automaticamente.
def crear_usuario_asovac(sender, **kwargs):

	user = kwargs["instance"]
	if kwargs["created"]:
		usuario_asovac = Usuario_asovac(usuario=user)
		usuario_asovac.save()

		first_usuario_asovac = Usuario_asovac.objects.count()
		roles = Rol.objects.count()
		list_areas= Area.objects.count()


		if list_areas == 0:
    		# Para cargar contenido para el area 1
			area= Area(id=1,nombre="Biociencias",descripcion="-")
			area.save()

			sub_area= Sub_area(nombre="Parasitología",descripcion="-",area_id=1)
			sub_area.save()

			sub_area= Sub_area(nombre="Biología Molecular",descripcion="-",area_id=1)
			sub_area.save()

			sub_area= Sub_area(nombre="Bioquímica",descripcion="-",area_id=1)
			sub_area.save()

			sub_area= Sub_area(nombre="Tecnología de Alimentos",descripcion="-",area_id=1)
			sub_area.save()

			sub_area= Sub_area(nombre="Ecología",descripcion="-",area_id=1)
			sub_area.save()

			sub_area= Sub_area(nombre="Medicina",descripcion="-",area_id=1)
			sub_area.save()

			sub_area= Sub_area(nombre="Inmunología",descripcion="-",area_id=1)
			sub_area.save()

			sub_area= Sub_area(nombre="Microbiología",descripcion="-",area_id=1)
			sub_area.save()

			sub_area= Sub_area(nombre="Farmacología",descripcion="-",area_id=1)
			sub_area.save()

    		# Para cargar contenido para el area 2
			area= Area(id=2,nombre="Ciencias Exactas",descripcion="-")
			area.save()

			sub_area= Sub_area(nombre="Matemática",descripcion="-",area_id=2)
			sub_area.save()

			sub_area= Sub_area(nombre="Química Organometálica",descripcion="-",area_id=2)
			sub_area.save()

			sub_area= Sub_area(nombre="Productos Naturales",descripcion="-",area_id=2)
			sub_area.save()

			sub_area= Sub_area(nombre="Farmacología",descripcion="-",area_id=2)
			sub_area.save()

			sub_area= Sub_area(nombre="Nanosistemas",descripcion="-",area_id=2)
			sub_area.save()

    		# Para cargar contenido para el area 3
			area= Area(id=3,nombre="Tecnología",descripcion="-")
			area.save()

			sub_area= Sub_area(nombre="Computación",descripcion="-",area_id=3)
			sub_area.save()

			sub_area= Sub_area(nombre="Ingeniería Electrónica y Biomédica",descripcion="-",area_id=3)
			sub_area.save()

    		# Para cargar contenido para el area 4
			area= Area(id=4,nombre="Ciencias Sociales",descripcion="-")
			area.save()

			sub_area= Sub_area(nombre="Ciencias Sociales",descripcion="-",area_id=4)
			sub_area.save()

			sub_area= Sub_area(nombre="Educación",descripcion="-",area_id=4)
			sub_area.save()

			# Para cargar contenido para el area 5
			area= Area(id=5,nombre="Congreso de la Sociedad Venezolana de Física",descripcion="-")
			area.save()

			sub_area= Sub_area(nombre="Física General",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Óptica y Plasmas",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Astronomía",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Física de Partículas Virtual",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Cosmología",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Materia Condensada Teórica",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Instrumentación",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Física Médica",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Física Nuclear",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Física de los Materiales",descripcion="-",area_id=5)
			sub_area.save()

			sub_area= Sub_area(nombre="Física del Espacio",descripcion="-",area_id=5)
			sub_area.save()


		#Esto asegura la creación de roles al momento de crear el primer usuario
		if first_usuario_asovac == 1 and roles == 0:
			rol = Rol(nombre="Admin", descripcion="Administrador")
			rol.save()

			rol = Rol(nombre="Coordinador General", descripcion ="CG")
			rol.save()

			rol = Rol(nombre="Coordinador de Área", descripcion ="CA")
			rol.save()

			rol = Rol(nombre="Árbitro de Subárea", descripcion ="AS")
			rol.save()

			rol = Rol(nombre="Autor",descripcion="Autor")
			rol.save()

			Rol_admin=Usuario_rol_in_sistema(status="1",rol_id="1",usuario_asovac_id=usuario_asovac.id)
			Rol_admin.save()
			usuario_asovac.sub_area.add(Sub_area.objects.get(id=1))
			usuario_asovac.save()
		else:
			if first_usuario_asovac == 1:
				Rol_admin=Usuario_rol_in_sistema(status="1",rol_id="1",usuario_asovac_id=usuario_asovac.id)
				Rol_admin.save()
				usuario_asovac.sub_area.add(Sub_area.objects.get(id=1))
				usuario_asovac.save()

post_save.connect(crear_usuario_asovac, sender=User)
