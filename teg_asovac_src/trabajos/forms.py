# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Trabajo #, Detalle_version_final


#Form para introducir datos de un trabajo, sea para editar o para crear
class TrabajoForm(forms.ModelForm):

	class Meta:
		model = Trabajo
		fields = ['titulo_espanol', 'titulo_ingles', 'palabras_clave', 'forma_presentacion', 'resumen', 'documento_inscrito', 'url_trabajo', 'archivo_trabajo']
		widgets = {
			'titulo_espanol': forms.TextInput(attrs={'placeholder': 'Ejemplo: Trabajo de prueba'}),
			'titulo_ingles': forms.TextInput(attrs={'placeholder': 'Ejemplo: Test Job'}),
			'palabras_clave': forms.TextInput(attrs={'placeholder': 'Introduzca sus palabras clave'}),
            'resumen': forms.Textarea(attrs={'placeholder': 'Introduzca su resumen aquí',
            														'rows':2 }),
            'url_trabajo': forms.TextInput(attrs={'placeholder': 'Ejemplo: www.google.com'}),
        }
	def __init__(self, *args, **kwargs):
		super(TrabajoForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'trabajo-form'
		self.helper.form_action = reverse('trabajos:trabajos')
		self.helper.form_tag = False
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.fields['titulo_espanol'].label = "Título español"
		self.fields['titulo_ingles'].label = "Título inglés"
		self.fields['forma_presentacion'].label = "Forma de presentación"
		self.fields['archivo_trabajo'].label = "Trabajo(PDF)"
		self.helper.layout = Layout(
			Div(	
				Div(
					Field('titulo_espanol',placeholder="Ejemplo: Titulo del trabajo"),
					Field('palabras_clave',placeholder="Introduzca sus palabras separadas con espacio"),
					Field('resumen', rows="4", placeholder="Introduzca el resumen del trabajo"),	
					HTML("<div class=\"form-group\"><div class=\"subareas-content\"><label class=\"control-label col-sm-6 requiredField\" for=\"area_select\">Área - Subarea del trabajo<span class=\"asteriskField\">*<span></label><div class=\"controls was-validated\" name=\"subarea\" ><select title = \"Seleccione el subarea\"  name=\"subarea_select\" class=\"form-control\" id=\"subarea_select\" required><option value=\"\" >Seleccione un Área - Subárea</option>{% for subarea in subarea_list %}<option data-area=\"{{subarea.area.id}}\"	value=\"{{subarea.id}}\" >{{subarea.area.nombre}} - {{ subarea.nombre }}</option>{% endfor %}</select></div></div></div>"),			
					css_class='col-sm-6',
					),
				Div(
					Field('titulo_ingles',placeholder="Ejemplo: Job's title"),
					Field('url_trabajo',placeholder="Ejemplo: www.github.com/YYYY"),
					'documento_inscrito',	
					Field('forma_presentacion',placeholder="Ejemplo: Fisica"),
					'archivo_trabajo',
					css_class='col-sm-6',
				),
				css_class='row'
			),
			HTML("<div class=\"col-sm-2 col-sm-offset-8\"><a href=\"#accordion\" class=\"btn btn-danger btn-block btn-lg\" data-toggle=\"collapse\">Cancelar</a></div><div class=\"col-sm-2\"><button type=\"button\" class=\"btn btn-primary btn-success btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#ModalCenter\">Guardar</button></div>"),
			HTML("<div class=\"modal fade\" id=\"ModalCenter\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"ModalCenterTitle\" aria-hidden=\"true\"><div class=\"modal-dialog modal-dialog-centered\" role=\"document\"><div class=\"modal-content\"><div class=\"modal-header\"><button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button><h3 class=\"modal-title\" id=\"ModalLongTitle\">Crear Trabajo</h3></div><div class=\"modal-body text-center content-modal\">¿Está seguro que desea crear el trabajo?</div><div class=\"modal-footer\"><button type=\"button\" class=\"btn btn-lg btn-danger\" data-dismiss=\"modal\">Cancelar</button><button type=\"submit\" class=\"btn btn-lg btn-primary\">Postular</button></div></div></div></div>"),
			)

	def clean_archivo_trabajo(self):
		trabajo = self.cleaned_data['archivo_trabajo']
		tamano_nombre_trabajo = len(trabajo.name)
		trabajo_extension = trabajo.name[tamano_nombre_trabajo - 3:].lower()
		print(trabajo_extension)
		if(trabajo_extension != "pdf"):
			raise forms.ValidationError(_("El archivo indicado no es pdf, por favor seleccione un archivo pdf."), code = "formato_archivo_incorrecto")
		return trabajo

#Form para editar datos de un trabajo, sea para editar o para crear
class EditTrabajoForm(forms.ModelForm):

	class Meta:
		model = Trabajo
		fields = ['titulo_espanol', 'titulo_ingles', 'palabras_clave', 'forma_presentacion', 'resumen', 'documento_inscrito', 'url_trabajo', 'archivo_trabajo']

	def __init__(self, *args, **kwargs):
		super(EditTrabajoForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'trabajo-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_tag = False
		self.fields['titulo_espanol'].label = "Título español"
		self.fields['titulo_ingles'].label = "Título inglés"
		self.fields['forma_presentacion'].label = "Forma de presentación"
		self.fields['archivo_trabajo'].label = "Archivo del trabajo (PDF)"
		self.helper.layout = Layout(
			Div(	
				Div(
					Field('titulo_espanol',placeholder="Ejemplo: Titulo del trabajo"),		
					Field('palabras_clave',placeholder="Introduzca sus palabras separadas con espacio"),
					Field('resumen', rows="4", placeholder="Introduzca el resumen del trabajo"),
					HTML("<div class=\"form-group\"><div class=\"subareas-content\"><label class=\"control-label col-sm-6 requiredField\" for=\"area_select\">Área - Subarea del trabajo<span class=\"asteriskField\">*<span></label><div class=\"controls was-validated\" name=\"subarea\" ><select title = \"Seleccione el subarea\"  name=\"subarea_select\" class=\"form-control\" id=\"subarea_select\" required>{% for subarea in subarea_list %}<option data-area=\"{{subarea.area.id}}\"	value=\"{{subarea.id}}\" {% if subarea_selected.id == subarea.id %} selected {% endif %}>{{subarea.area.nombre}} - {{ subarea.nombre }}</option>{% endfor %}</select></div></div></div>"),	
					css_class='col-sm-6',
					),
				Div(
					Field('titulo_ingles',placeholder="Ejemplo: Job's title"),
					Field('url_trabajo',placeholder="Ejemplo: www.github.com/YYYY"),
					'documento_inscrito',
					Field('forma_presentacion',placeholder="Ejemplo: Fisica"),	
					'archivo_trabajo',	
					css_class='col-sm-6',
				),
				css_class='row'
			)
		)

	def clean_archivo_trabajo(self):
		trabajo = self.cleaned_data['archivo_trabajo']
		tamano_nombre_trabajo = len(trabajo.name)
		trabajo_extension = trabajo.name[tamano_nombre_trabajo - 3:].lower()
		print(trabajo_extension)
		if(trabajo_extension != "pdf"):
			raise forms.ValidationError(_("El archivo indicado no es pdf, por favor seleccione un archivo pdf."), code = "formato_archivo_incorrecto")
		return trabajo

class MessageForm(forms.Form):
    motivo_rechazo = forms.CharField(label='Motivos del rechazo', widget = forms.Textarea, max_length=100)
    def __init__(self, *args, **kwargs):
		super(MessageForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'message-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_tag = False