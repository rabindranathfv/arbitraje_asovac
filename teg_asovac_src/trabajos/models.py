# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .validators import validate_file_extension
from datetime import datetime

from main_app.models import Area, Sub_area
from sesiones.models import Sesion
# Create your models here.



CHOICES_TIPO_PRESENTACION_TRABAJO = (	('Presencial', 'Presencial'),
								('Virtual', 'Virtual'),
	)


"""""""""""""""""""""""""""
Trabajo Model
"""""""""""""""""""""""""""
#Estaba en el modelo
def job_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/trabajos/<trabajo_id>.pdf
	if(instance.id):
		return 'trabajos/{0}.pdf'.format(instance.id)
	#elif Trabajo:
	#	return 'trabajos/1.pdf'	
	else:
		
		future_id = Trabajo.objects.count()+ 1
		return 'trabajos/' + str(future_id) + '.pdf'
		

class Trabajo(models.Model):

	# autor_id = models.ManyToManyField('autores.Autor',through='Autores_trabajos')
	# autor_id = models.ManyToManyField('autores.Autor')
	arbitro = models.ManyToManyField('arbitrajes.Arbitro',through='Trabajo_arbitro')
	subareas = models.ManyToManyField(Sub_area) #Se permiten hasta 3 subareas
	trabajo_version= models.ForeignKey('self', null=True, blank=True)
	sesion = models.ForeignKey('sesiones.Sesion', null=True, blank = True)

	estatus = models.CharField(max_length=20, default="Pendiente")
	codigo = models.CharField(max_length=20, blank = True)
	titulo_espanol = models.CharField(max_length=100)
	titulo_ingles = models.CharField(max_length=100, blank = True)
	palabras_clave = models.CharField(max_length=60, blank = True)
	forma_presentacion = models.CharField(max_length=20,choices = CHOICES_TIPO_PRESENTACION_TRABAJO)
	resumen = models.TextField(max_length=255)
	documento_inscrito =  models.CharField(max_length=100,blank=True)
	observaciones = models.TextField(blank = True)
	url_trabajo = models.URLField(max_length=255,blank=True)
	version = models.CharField(max_length=20,blank=True)
	archivo_trabajo = models.FileField(upload_to = job_directory_path,validators=[validate_file_extension])#upload_to = job_directory_path,
	requiere_arbitraje= models.BooleanField(default=False)
	padre =  models.IntegerField(default=0)
	confirmacion_pago= models.CharField(max_length=20, default="Por Revisar")
	def __str__(self):
    		return self.titulo_espanol.encode('utf-8', errors='replace')

class Trabajo_arbitro (models.Model):
	arbitro = models.ForeignKey('arbitrajes.Arbitro')
	trabajo = models.ForeignKey('Trabajo')
	fin_arbitraje= models.BooleanField(default = False)
	invitacion= models.BooleanField()
	comentario_autor= models.TextField(blank=True)
	arbitraje_resultado = models.CharField(max_length=50,blank=True)
	fecha_arbitraje = models.DateField(blank=True, null=True)

	def __str__(self):
    		return "{} {} - {}".format(self.arbitro.nombres,self.arbitro.apellidos, self.trabajo.titulo_espanol).encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Detalle_version_final Model
"""""""""""""""""""""""""""
class Detalle_version_final(models.Model):
	
	arbitraje = models.OneToOneField('arbitrajes.Arbitraje', blank = True, null = True)
	trabajo = models.OneToOneField(Trabajo, on_delete = models.CASCADE)

	estatus_final = models.CharField(max_length=20, default="Pendiente")
	observaciones = models.TextField(max_length=255, blank = True)
	se_recibio_version_final_corregida = models.BooleanField(default=False)
	fecha_envio_version_final = models.DateField(default = datetime.now)
	se_recibio_version_final_presentacion = models.BooleanField(default=False)
	url_version_final_presentacion = models.CharField(max_length=35)
	fecha_envio_version_final_presentacion = models.DateField(blank = True, null = True)

	def __str__(self):
		return self.trabajo.titulo_espanol#.encode('utf-8', errors='replace')

