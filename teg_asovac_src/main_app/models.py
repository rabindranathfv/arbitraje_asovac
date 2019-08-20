# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import now as timezone_now


# Create your models here.

# Este es un diccionario con los estados numericos y en string de los arbitrajes.
estados_arbitraje = {
    '0':'Desactivado',
    '1':'Iniciado',
    '2':'En Selección y Asignación de Coordinadores de Área',
    '3':'En Carga de Trabajos',
    '4':'En Asignación de Trabajos a las Áreas',
    '5':'En Arbitraje',
    '6':'En Cierre de Arbitraje',
    '7':'En Asignación de Sesiones',
    '8':'En Resumen',
}

def upload_to(instance, filename):
    now = timezone_now()
    filename_list = filename.split('.')
    ext = filename_list[-1].lower()
    path = "sistemas_asovac/%s/%s.%s" % (instance.id, now.strftime('%Y%m%d%H%M%S'), ext)
    return path

"""""""""""""""""""""""""""
Rol Model
"""""""""""""""""""""""""""
class Rol(models.Model):

    nombre = models.CharField(
        max_length=80
    )
    descripcion = models.TextField(
        max_length=255
    )

    def __str__(self):
        return self.nombre.encode('utf-8', errors='replace')

"""""""""""""""""""""""""""
Area Model
"""""""""""""""""""""""""""
class Area(models.Model):

    nombre = models.CharField(
        max_length=100
    )
    codigo = models.CharField(
        max_length=10,
        blank=True
    )
    descripcion = models.TextField(
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.nombre.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Sub_area Model
"""""""""""""""""""""""""""
class Sub_area(models.Model):

    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE
    )
    nombre = models.CharField(
        max_length=80
    )
    codigo = models.CharField(
        max_length=10,
        blank=True
    )
    descripcion = models.TextField(
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.nombre.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Sistema_asovac Model
"""""""""""""""""""""""""""
class Sistema_asovac(models.Model):

    nombre = models.CharField(
        max_length=80
    )
    descripcion = models.TextField(
        max_length=255
    )
    fecha_inicio_arbitraje = models.DateField()
    fecha_fin_arbitraje = models.DateField()
    coordinador_general = models.ForeignKey(
        'Usuario_asovac',
        blank=True,
        null=True
    )
    estado_arbitraje = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(8)
        ]
    )
    clave_maestra_coordinador_area = models.CharField(
        max_length=100,
        blank=True
    )
    clave_maestra_arbitro_area = models.CharField(
        max_length=100,
        blank=True
    )
    clave_maestra_coordinador_general = models.CharField(
        max_length=100,
        blank=True
    )
    clave_maestra_arbitro_subarea = models.CharField(
        max_length=100,
        blank=True
    )
    porcentaje_iva = models.SmallIntegerField()
    monto_pagar_trabajo = models.IntegerField()
    cabecera = models.CharField(
        'URL Imagen de Cabecera',
        max_length=255,
        default='https://i.imgur.com/G1PXYZU.jpg'
    )
    color_fondo_pie = models.CharField(
        max_length=7,
        default='#222',
        validators=[
            RegexValidator(
                r'^(\#[a-fA-F0-9]{6}|\#[a-fA-F0-9]{3})?$',
                'Este es un código de color inválido. Debe ser un código de color hexadecimal html ej. #000000'
            )
        ]
    )
    color_letras_pie = models.CharField(
        max_length=7,
        default='#FFF',
        validators=[
            RegexValidator(
                r'^(\#[a-fA-F0-9]{6}|\#[a-fA-F0-9]{3})?$',
                'Este es un código de color inválido. Debe ser un código de color hexadecimal html ej. #000000'
            )
        ]
    )
    autoridad1 = models.CharField(
        max_length=100,
        default='Nombre Autoridad1,Título en Organización,Nombre Organización'
    )
    firma1 = models.ImageField(
        upload_to=upload_to,
        default='default/signature_sample.jpg'
    )
    autoridad2 = models.CharField(
        max_length=100,
        default='Nombre Autoridad2,Título en Organización,Nombre Organización'
    )
    firma2 = models.ImageField(
        upload_to=upload_to,
        default='default/signature_sample.jpg'
    )
    logo = models.ImageField(
        upload_to=upload_to,
        default='default/AsoVac_Logo.jpg'
    )

    def __str__(self):
        return self.nombre.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Usuario_asovac Model
"""""""""""""""""""""""""""
class Usuario_asovac(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    sub_area = models.ManyToManyField(
        Sub_area,
        blank=True
    )

    usuario_activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return "{} {}".format(self.usuario.first_name,
                              self.usuario.last_name).encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Usuario_rol_in_sistema Model
"""""""""""""""""""""""""""
class Usuario_rol_in_sistema(models.Model):

    rol = models.ForeignKey(
        Rol
    )
    sistema_asovac = models.ForeignKey(
        Sistema_asovac,
        blank=True,
        null=True
    )
    usuario_asovac = models.ForeignKey(
        Usuario_asovac
    )

    status = models.BooleanField(
        default=True
    )

    def __str__(self):
        return "{} {} {}".format(self.usuario_asovac.usuario.first_name,
                                 self.usuario_asovac.usuario.last_name,
                                 self.rol.descripcion).encode('utf-8', errors='replace')




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
            area= Area(id=1,nombre="Biociencias",descripcion="-",codigo="BC")
            area.save()

            sub_area= Sub_area(nombre="Parasitología",descripcion="-",area_id=1,codigo="PAR")
            sub_area.save()

            sub_area= Sub_area(nombre="Biología Molecular",descripcion="-",area_id=1,codigo="BMOL")
            sub_area.save()

            sub_area= Sub_area(nombre="Bioquímica",descripcion="-",area_id=1,codigo="BQM")
            sub_area.save()

            sub_area= Sub_area(nombre="Tecnología de Alimentos",descripcion="-",area_id=1,codigo="TCA")
            sub_area.save()

            sub_area= Sub_area(nombre="Ecología",descripcion="-",area_id=1,codigo="ECO")
            sub_area.save()

            sub_area= Sub_area(nombre="Medicina",descripcion="-",area_id=1,codigo="MED")
            sub_area.save()

            sub_area= Sub_area(nombre="Inmunología",descripcion="-",area_id=1,codigo="INM")
            sub_area.save()

            sub_area= Sub_area(nombre="Microbiología",descripcion="-",area_id=1,codigo="MICB")
            sub_area.save()

            sub_area= Sub_area(nombre="Farmacología",descripcion="-",area_id=1,codigo="FMC")
            sub_area.save()

            # Para cargar contenido para el area 2
            area= Area(id=2,nombre="Ciencias Exactas",descripcion="-",codigo="CE")
            area.save()

            sub_area= Sub_area(nombre="Matemática",descripcion="-",area_id=2,codigo="MAT")
            sub_area.save()

            sub_area= Sub_area(nombre="Química Organometálica",descripcion="-",area_id=2,codigo="OM")
            sub_area.save()

            sub_area= Sub_area(nombre="Productos Naturales",descripcion="-",area_id=2,codigo="PN")
            sub_area.save()

            sub_area= Sub_area(nombre="Farmacología",descripcion="-",area_id=2,codigo="FMC")
            sub_area.save()

            sub_area= Sub_area(nombre="Nanosistemas",descripcion="-",area_id=2,codigo="NS")
            sub_area.save()

            # Para cargar contenido para el area 3
            area= Area(id=3,nombre="Tecnología",descripcion="-",codigo="TEC")
            area.save()

            sub_area= Sub_area(nombre="Computación",descripcion="-",area_id=3,codigo="COMP")
            sub_area.save()

            sub_area= Sub_area(nombre="Ingeniería Electrónica y Biomédica",descripcion="-",area_id=3,codigo="IEB")
            sub_area.save()

            # Para cargar contenido para el area 4
            area= Area(id=4,nombre="Ciencias Sociales",descripcion="-",codigo="CS")
            area.save()

            sub_area= Sub_area(nombre="Ciencias Sociales 1",descripcion="-",area_id=4,codigo="CS1")
            sub_area.save()

            sub_area= Sub_area(nombre="Educación 1",descripcion="-",area_id=4,codigo="EDU1")
            sub_area.save()

            # Para cargar contenido para el area 5
            area= Area(id=5,nombre="Congreso de la Sociedad Venezolana de Física",descripcion="-",codigo="CF")
            area.save()

            sub_area= Sub_area(nombre="Física General",descripcion="-",area_id=5,codigo="FGEN")
            sub_area.save()

            sub_area= Sub_area(nombre="Óptica y Plasmas",descripcion="-",area_id=5,codigo="OPP")
            sub_area.save()

            sub_area= Sub_area(nombre="Astronomía",descripcion="-",area_id=5,codigo="AST")
            sub_area.save()

            sub_area= Sub_area(nombre="Física de Partículas Virtual",descripcion="-",area_id=5,codigo="FPART-V")
            sub_area.save()

            sub_area= Sub_area(nombre="Cosmología",descripcion="-",area_id=5,codigo="COSM")
            sub_area.save()

            sub_area= Sub_area(nombre="Materia Condensada Teórica",descripcion="-",area_id=5,codigo="MCT")
            sub_area.save()

            sub_area= Sub_area(nombre="Instrumentación",descripcion="-",area_id=5,codigo="INST")
            sub_area.save()

            sub_area= Sub_area(nombre="Física Médica",descripcion="-",area_id=5,codigo="FMED")
            sub_area.save()

            sub_area= Sub_area(nombre="Física Nuclear",descripcion="-",area_id=5,codigo="FNU")
            sub_area.save()

            sub_area= Sub_area(nombre="Física de los Materiales",descripcion="-",area_id=5,codigo="FMAT")
            sub_area.save()
            
            sub_area= Sub_area(nombre="Física Teórica",descripcion="-",area_id=5,codigo="FTEO")
            sub_area.save()

            sub_area= Sub_area(nombre="Física del Espacio",descripcion="-",area_id=5,codigo="FESP")
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
