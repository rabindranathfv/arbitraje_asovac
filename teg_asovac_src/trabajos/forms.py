# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from django.core.urlresolvers import reverse

from .models import Trabajo, Detalle_version_final


#Form para introducir datos de un trabajo, sea para editar o para crear
class TrabajoForm(forms.ModelForm):

	class Meta:
		model = Trabajo
		fields = ['titulo_espanol', 'titulo_ingles', 'palabras_clave', 'forma_presentacion', 'area', 'subarea1', 'subarea2', 'subarea3', 'resumen', 'documento_inscrito', 'observaciones', 'url_trabajo', 'version', 'archivo_trabajo']

	def __init__(self, *args, **kwargs):
		super(TrabajoForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'trabajo-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['titulo_espanol'].label = "Título español"
		self.fields['titulo_ingles'].label = "Título inglés"
		self.fields['forma_presentacion'].label = "Forma de presentación"
		self.fields['area'].label = "Área"
		self.fields['subarea1'].label = "Subárea 1"
		self.fields['subarea2'].label = "Subárea 2"
		self.fields['subarea3'].label = "Subárea 3"
		self.fields['version'].label = "Versión"
		self.fields['archivo_trabajo'].label = "Archivo del trabajo (PDF)"
		self.helper.layout = Layout(
			Div(	
				Div(
					Field('titulo_espanol',placeholder="Ejemplo: Titulo del trabajo"),
					Field('titulo_ingles',placeholder="Ejemplo: Job's title"),
					Field('palabras_clave',placeholder="Introduzca sus palabras separadas con espacio"),
					Field('forma_presentacion',placeholder="Ejemplo: Fisica"),
					Field('area',placeholder="Ejemplo: Computación"),
					Field('subarea1',placeholder="Ejemplo: Gráfica"),
					Field('subarea2',placeholder="Ejemplo: Inteligencia Artificial"),
					Field('subarea3',placeholder="Ejemplo: Aplicaciones en Internet"),
					'archivo_trabajo',
					css_class='col-sm-6',
					),
				Div(
					Field('version',placeholder="Ejemplo: 1.0"),
					Field('url_trabajo',placeholder="Ejemplo: www.github.com/YYYY"),
					'documento_inscrito',
					Field('resumen', rows="4", placeholder="Introduzca el resumen del trabajo"),			
					Field('observaciones', rows="4", placeholder="Introduzca sus observaciones"),
					css_class='col-sm-6',
				),
				css_class='row'
			),
			HTML("<div class=\"col-sm-2 col-sm-offset-8\"><a href=\"#accordion\" class=\"btn btn-danger btn-block btn-lg\" data-toggle=\"collapse\">Cancelar</a></div><div class=\"col-sm-2\"><button type=\"button\" class=\"btn btn-primary btn-success btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#ModalCenter\">Guardar</button></div>"),
			HTML("<div class=\"modal fade\" id=\"ModalCenter\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"ModalCenterTitle\" aria-hidden=\"true\"><div class=\"modal-dialog modal-dialog-centered\" role=\"document\"><div class=\"modal-content\"><div class=\"modal-header\"><h3 class=\"modal-title\" id=\"ModalLongTitle\">Crear Trabajo</h5><button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div><div class=\"modal-body text-center content-modal\">¿Está seguro que desea crear el trabajo?</div><div class=\"modal-footer\"><button type=\"button\" class=\"btn btn-secondary btn-danger\" data-dismiss=\"modal\">Cancelar</button><button type=\"submit\" class=\"btn btn-primary btn-success\">Postular</button></div></div></div></div>"),
			)


#Form para editar datos de un trabajo, sea para editar o para crear
class EditTrabajoForm(forms.ModelForm):

	class Meta:
		model = Trabajo
		fields = ['titulo_espanol', 'titulo_ingles', 'palabras_clave', 'forma_presentacion', 'area', 'subarea1', 'subarea2', 'subarea3', 'resumen', 'documento_inscrito', 'observaciones', 'url_trabajo', 'version', 'archivo_trabajo']

	def __init__(self, *args, **kwargs):
		super(EditTrabajoForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'trabajo-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['titulo_espanol'].label = "Título español"
		self.fields['titulo_ingles'].label = "Título inglés"
		self.fields['forma_presentacion'].label = "Forma de presentación"
		self.fields['area'].label = "Área"
		self.fields['subarea1'].label = "Subárea 1"
		self.fields['subarea2'].label = "Subárea 2"
		self.fields['subarea3'].label = "Subárea 3"
		self.fields['version'].label = "Versión"
		self.fields['archivo_trabajo'].label = "Archivo del trabajo (PDF)"
		self.helper.layout = Layout(
			Div(	
				Div(
					Field('titulo_espanol',placeholder="Ejemplo: Titulo del trabajo"),
					Field('titulo_ingles',placeholder="Ejemplo: Job's title"),
					Field('palabras_clave',placeholder="Introduzca sus palabras separadas con espacio"),
					Field('forma_presentacion',placeholder="Ejemplo: Fisica"),
					Field('area',placeholder="Ejemplo: Computación"),
					Field('subarea1',placeholder="Ejemplo: Gráfica"),
					Field('subarea2',placeholder="Ejemplo: Inteligencia Artificial"),
					Field('subarea3',placeholder="Ejemplo: Aplicaciones en Internet"),
					'archivo_trabajo',
					css_class='col-sm-6',
					),
				Div(
					Field('version',placeholder="Ejemplo: 1.0"),
					Field('url_trabajo',placeholder="Ejemplo: www.github.com/YYYY"),
					'documento_inscrito',
					Field('resumen', rows="4", placeholder="Introduzca el resumen del trabajo"),			
					Field('observaciones', rows="4", placeholder="Introduzca sus observaciones"),
					css_class='col-sm-6',
				),
				css_class='row'
			),
			HTML("<div class=\"col-sm-2 col-sm-offset-8\"><a href=\"{% url 'trabajos:trabajos' %}\" class=\"btn btn-danger btn-block btn-lg\" >Cancelar</a></div><div class=\"col-sm-2\"><button type=\"button\" class=\"btn btn-primary btn-success btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#ModalCenter\">Guardar</button></div>"),
			HTML("<div class=\"modal fade\" id=\"ModalCenter\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"ModalCenterTitle\" aria-hidden=\"true\"><div class=\"modal-dialog modal-dialog-centered\" role=\"document\"><div class=\"modal-content\"><div class=\"modal-header\"><h3 class=\"modal-title\" id=\"ModalLongTitle\">Editar Trabajo</h5><button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div><div class=\"modal-body text-center content-modal\">¿Está seguro que desea editar el trabajo?</div><div class=\"modal-footer\"><button type=\"button\" class=\"btn btn-secondary btn-danger\" data-dismiss=\"modal\">Cancelar</button><button type=\"submit\" class=\"btn btn-primary btn-success\">Postular</button></div></div></div></div>"),
			)

#Form para colocar observaciones a la versión final del trabajo
class AutorObservationsFinalVersionJobForm(forms.ModelForm):

	class Meta:
		model = Detalle_version_final
		fields = ['observaciones']

	def __init__(self, *args, **kwargs):
		super(AutorObservationsFinalVersionJobForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'job-observations-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['observaciones'].label = "Observaciones"
		self.fields['observaciones'].widget.attrs['rows'] = 4

