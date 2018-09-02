# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .validators import validate_file_extension
# Create your models here.


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
	arbitro_id = models.ManyToManyField('arbitrajes.Arbitro',blank=True)


	estatus = models.CharField(max_length=20, default="Pendiente")
	titulo_espanol = models.CharField(max_length=40)
	titulo_ingles = models.CharField(max_length=40, blank = True)
	palabras_clave = models.CharField(max_length=40, blank = True)
	forma_presentacion = models.CharField(max_length=40)
	area = models.CharField(max_length=20)
	subarea1 = models.CharField(max_length=20)
	subarea2 = models.CharField(max_length=20, blank = True)
	subarea3 = models.CharField(max_length=20, blank = True)
	resumen = models.TextField(max_length=255)
	documento_inscrito =  models.CharField(max_length=100,blank=True)
	observaciones = models.TextField(max_length=255, blank = True)
	url_trabajo = models.CharField(max_length=255,blank=True)
	version = models.CharField(max_length=20,blank=True)
	archivo_trabajo = models.FileField(upload_to = job_directory_path,validators=[validate_file_extension])#upload_to = job_directory_path,
	def __str__(self):
    		return self.titulo_espanol#.encode('utf-8', errors='replace')


"""""""""""""""""""""""""""
Detalle_version_final Model
"""""""""""""""""""""""""""
class Detalle_version_final(models.Model):
	
	arbitraje = models.OneToOneField('arbitrajes.Arbitraje', blank = True)
	trabajo = models.OneToOneField(Trabajo, on_delete = models.CASCADE)

	estatus_final = models.CharField(max_length=20)
	observaciones = models.TextField(max_length=255, blank = True)
	se_recibio_version_final_corregida = models.BooleanField(default=False)
	url_version_final_trabajo = models.CharField(max_length=35, blank = True)
	fecha_envio_version_final = models.DateField()
	se_recibio_version_final_presentacion = models.BooleanField(default=False)
	url_version_final_presentacion = models.CharField(max_length=35)
	fecha_envio_version_final_presentacion = models.DateField()
	#archivo_trabajo_final = models.FileField(validators=[validate_file_extension])
	def __str__(self):
		return self.url_version_final_trabajo#.encode('utf-8', errors='replace')


