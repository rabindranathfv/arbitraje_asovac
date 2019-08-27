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
    ciudad = models.CharField(
        max_length=50,
        default='Caracas'
    )
    numero_romano = models.CharField(
        max_length=15,
        default='LXVII'
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

        # Esto asegura la creación de un rol de administrador al momento de crear el primer usuario
        # usualmente un superuser.
        usuario_asovac_count = Usuario_asovac.objects.count()
        if usuario_asovac_count <= 1:
            rol_admin = Usuario_rol_in_sistema(status="1", rol_id="1", usuario_asovac_id=usuario_asovac.id)
            rol_admin.save()
            usuario_asovac.sub_area.add(Sub_area.objects.get(id=1))
            usuario_asovac.save()

post_save.connect(crear_usuario_asovac, sender=User)
