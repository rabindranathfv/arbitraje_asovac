# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from django.core.urlresolvers import reverse

from .models import Trabajo

class TrabajoForm(forms.ModelForm):

	class Meta:
		model = Trabajo
		fields = ['titulo_espanol', 'titulo_ingles', 'palabras_clave', 'forma_presentacion', 'area', 'subarea1', 'subarea2', 'subarea3', 'resumen', 'documento_inscrito', 'observaciones', 'url_trabajo', 'version']

	def __init__(self, *args, **kwargs):
		super(TrabajoForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'trabajo-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['titulo_espanol'].label = "Titulo español"
		self.fields['titulo_ingles'].label = "Titulo inglés"
		self.fields['forma_presentacion'].label = "Forma de presentación"
		self.fields['area'].label = "Área"
		self.fields['subarea1'].label = "Subárea 1"
		self.fields['subarea2'].label = "Subárea 2"
		self.fields['subarea3'].label = "Subárea 3"
		self.fields['version'].label = "Versión"
		self.helper.layout = Layout(
			Div(	
				Div(
					'titulo_espanol',
					'titulo_ingles',
					'palabras_clave',
					'forma_presentacion',
					'area',
					'subarea1',
					'subarea2',
					'subarea3',
					css_class='col-sm-6',
					),
				Div(
					'version',
					'url_trabajo',
					'documento_inscrito',
					Field('resumen', rows="4"),			
					Field('observaciones', rows="4"),
					css_class='col-sm-6',
				),
				css_class='row'
			),
			#Div(
			 #	Div(
			#		HTML("<a href=\"#accordion\" class=\"btn btn-danger btn-block btn-lg\" data-toggle=\"collapse\">Cancelar</a> "),
			#	css_class='col-sm-2 col-sm-offset-8'),
             #   Div(
                    #Submit('submit', 'Crear', css_class='btn-success btn-lg btn-block'),css_class='col-sm-2'),
              #      HTML("<button type=\"button\" class=\"btn btn-primary btn-success btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#ModalCenter\">Guardar</button>"),css_class='col-sm-2'),
            #css_class='row'),
			)
