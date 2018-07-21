# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from django.core.urlresolvers import reverse

from trabajos.models import Trabajo
from .models import Datos_pagador, Pago, Factura

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
					'version',
					'url_trabajo',
					'documento_inscrito',
					css_class='col-sm-6',
					),
				Div(
					Field('resumen', rows="4"),			
					Field('observaciones', rows="4"),
					css_class='col-sm-6',
				),
				css_class='row'
			),
			Div(
			 	Div(
					HTML("<a href=\"{% url 'main_app:home' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a> "),
				css_class='col-sm-2 col-sm-offset-8'),
                Div(
                    #Submit('submit', 'Crear', css_class='btn-success btn-lg btn-block'),css_class='col-sm-2'),
                    HTML("<button type=\"button\" class=\"btn btn-primary btn-success btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#ModalCenter\">Guardar</button>"),css_class='col-sm-2'),
            css_class='row'),
			)


class DatosPagadorForm(forms.ModelForm):

	class Meta:
		model = Datos_pagador
		fields = ['cedula', 'nombre', 'apellido', 'pasaporte_rif', 'telefono_oficina', 'telefono_habitacion_celular', 'direccion_fiscal']

	def __init__(self, *args, **kwargs):
		super(DatosPagadorForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'datos-pagador-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['cedula'].label = "Cédula"
		self.fields['nombre'].label = "Nombre"
		self.fields['apellido'].label = "Apellido"
		self.fields['pasaporte_rif'].label = "Pasaporte/RIF"
		self.fields['telefono_oficina'].label = "Teléfono de Oficina"
		self.fields['telefono_habitacion_celular'].label = "Teléfono de habitación/Celular"
		self.fields['direccion_fiscal'].label = "Dirección Fiscal"
		self.helper.layout = Layout(
			'cedula',
			'nombre',
			'apellido',
			'pasaporte_rif',
			'telefono_oficina',
			'telefono_habitacion_celular',
			'direccion_fiscal',
		)


class PagoForm(forms.ModelForm):

	class Meta:
		model = Pago
		fields = ['tipo_pago', 'numero_cuenta_origen', 'banco_origen', 'numero_transferencia', 'numero_cheque', 'fecha_pago', 'observaciones', 'comprobante_pago']

	def __init__(self, *args, **kwargs):
		super(PagoForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'pago-form'
		self.helper.form_method = 'post'
		self.helper.form_class =  'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['tipo_pago'].label = "Tipo de pago"
		self.fields['numero_cuenta_origen'].label = "Numero de cuenta origen"
		self.fields['banco_origen'].label = "Banco origen"
		self.fields['numero_transferencia'].label = "Número de transferencia"
		self.fields['numero_cheque'].label = "Número de cheque"
		self.fields['fecha_pago'].label = "Fecha del pago"
		self.fields['observaciones'].label = "Observaciones"
		self.fields['comprobante_pago'].label = "Comprobante de pago"
		self.helper.layout = Layout(
			'tipo_pago',
			'numero_cuenta_origen',
			'banco_origen',
			'numero_transferencia',
			'numero_cheque',
			'fecha_pago',
			'observaciones',
			'comprobante_pago',
		)

class FacturaForm(forms.ModelForm):
	
	class Meta:
		model = Factura
		fields = ['monto_subtotal','fecha_emision','monto_total', 'iva']

	def __init__(self, *args, **kwargs):
		super(FacturaForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'factura-form'
		self.helper.form_method = 'post'
		self.helper.form_class =  'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['monto_subtotal'].label = "Monto Subtotal"
		self.fields['fecha_emision'].label = "Fecha de emisión"
		self.fields['monto_total'].label = "Monto Total"
		self.fields['iva'].label = "IVA"
		self.helper.layout = Layout(
			'monto_subtotal',
			'fecha_emision',
			'monto_total',
			'iva',
			Div(
                Div(
					Submit('submit', 'Crear', css_class='btn-success btn-lg btn-block'),css_class='col-sm-2 col-sm-offset-10'),css_class="row"),
			)
			
