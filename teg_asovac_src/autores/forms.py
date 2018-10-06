# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from django.core.urlresolvers import reverse

from trabajos.models import Trabajo
from .models import Datos_pagador, Pago, Factura, Autores_trabajos

# Form para añadir autores a un trabajo
class AddAuthorToJobForm(forms.ModelForm):

	class Meta:
		model = Autores_trabajos
		fields = ['es_ponente', 'es_coautor']

	correo = forms.EmailField()
	
	def __init__(self, *args, **kwargs):
		super(AddAuthorToJobForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'add-author-to-job-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-4'
		self.helper.field_class = 'col-sm-8'
		self.fields['correo'].label = "Correo"
		self.fields['es_ponente'].label = "¿Es ponente?"
		self.fields['es_coautor'].label = "¿Es coautor?"
		self.helper.layout = Layout(
			'correo',
			'es_ponente',
			'es_coautor',
			)

# Form para datos del pagador
class DatosPagadorForm(forms.ModelForm):

	class Meta:
		model = Datos_pagador
		fields = ['categorias_pago','cedula', 'nombres', 'apellidos', 'pasaporte_rif', 'telefono_oficina', 'telefono_habitacion_celular', 'direccion_fiscal']
		widgets = {
            'categorias_pago': forms.TextInput(attrs={'placeholder': 'Personal, terceros o instituciones'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Ejemplo:12345678'}),
            'nombres': forms.TextInput(attrs={'placeholder': 'Ejemplo: Juan Enrique'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Ejemplo:Carrasco Lopez'}),
            'pasaporte_rif': forms.TextInput(attrs={'placeholder': 'Ejemplo:12345678-1'}),
            'telefono_oficina': forms.TextInput(attrs={'placeholder': 'Formato: xxxx-xxx-xx-xx'}),
            'telefono_habitacion_celular': forms.TextInput(attrs={'placeholder': 'Formato: xxxx-xxx-xx-xx'}),
            'direccion_fiscal': forms.Textarea(attrs={'placeholder': 'Introduzca su dirección aquí', 'rows':'4'}),
        }


	def __init__(self, *args, **kwargs):
		super(DatosPagadorForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'datos-pagador-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['categorias_pago'].label = "Categoría del pago"
		self.fields['cedula'].label = "Cédula"
		self.fields['nombres'].label = "Nombres"
		self.fields['apellidos'].label = "Apellidos"
		self.fields['pasaporte_rif'].label = "Pasaporte/RIF"
		self.fields['telefono_oficina'].label = "Teléfono de Oficina"
		self.fields['telefono_habitacion_celular'].label = "Teléfono de habitación/Celular"
		self.fields['direccion_fiscal'].label = "Dirección Fiscal"



# Form para editar datos del pagador
class EditarDatosPagadorForm(forms.ModelForm):

	class Meta:
		model = Datos_pagador
		fields = ['cedula', 'nombres', 'apellidos', 'pasaporte_rif', 'telefono_oficina', 'telefono_habitacion_celular', 'direccion_fiscal']

	def __init__(self, *args, **kwargs):
		super(EditarDatosPagadorForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'datos-pagador-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['cedula'].label = "Cédula"
		self.fields['nombres'].label = "Nombre"
		self.fields['apellidos'].label = "Apellido"
		self.fields['pasaporte_rif'].label = "Pasaporte/RIF"
		self.fields['telefono_oficina'].label = "Teléfono de Oficina"
		self.fields['telefono_habitacion_celular'].label = "Teléfono de habitación/Celular"
		self.fields['direccion_fiscal'].label = "Dirección Fiscal"
		self.helper.layout = Layout(
			'cedula',
			'nombres',
			'apellidos',
			'pasaporte_rif',
			'telefono_oficina',
			'telefono_habitacion_celular',
			'direccion_fiscal',
			Div(
                Div(
					HTML("<a href=\"{% url 'autores:postular_trabajo' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),css_class='col-sm-2  col-sm-offset-8'),
                Div(
                	Submit('submit', 'Crear', css_class='btn-success btn-lg btn-block'),css_class='col-sm-2'),
                css_class="row"),
			)
		

# Form para vista de pago
class PagoForm(forms.ModelForm):

	class Meta:
		model = Pago
		fields = ['tipo_pago', 'numero_cuenta_origen', 'banco_origen', 'numero_transferencia', 'numero_cheque', 'fecha_pago', 'observaciones', 'comprobante_pago']
		widgets = {
            'tipo_pago': forms.TextInput(attrs={'placeholder': 'Transferencia o cheque'}),
            'numero_cuenta_origen': forms.TextInput(attrs={'placeholder': 'XXXXXXXXXXXXXXXXXXXX'}),
            'banco_origen': forms.TextInput(attrs={'placeholder': 'Ejemplo: Banco de Venezuela'}),
            'numero_transferencia': forms.TextInput(attrs={'placeholder': 'Ejemplo: XXXXXXXXXX'}),
            'numero_cheque': forms.TextInput(attrs={'placeholder': 'Ejemplo: XXXXXXXXXX'}),
            'fecha_pago': forms.TextInput(attrs={'placeholder': 'Formato: DD/MM/AAAA'}),
            'observaciones': forms.TextInput(attrs={'placeholder': 'Introduzca sus observaciones'}),
        }
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



# Form para vista de pago
class EditarPagoForm(forms.ModelForm):

	class Meta:
		model = Pago
		fields = ['tipo_pago', 'numero_cuenta_origen', 'banco_origen', 'numero_transferencia', 'numero_cheque', 'fecha_pago', 'observaciones', 'comprobante_pago']

	def __init__(self, *args, **kwargs):
		super(EditarPagoForm,self).__init__(*args, **kwargs)
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
			Div(
                Div(
					HTML("<a href=\"{% url 'autores:postular_trabajo' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),css_class='col-sm-2  col-sm-offset-8'),
                Div(
                	Submit('submit', 'Crear', css_class='btn-success btn-lg btn-block'),css_class='col-sm-2'),
                css_class="row"),
			)
		


# Form para vista de Factura
class FacturaForm(forms.ModelForm):
	
	class Meta:
		model = Factura
		fields = ['monto_subtotal','fecha_emision', 'iva', 'monto_total']
		widgets = {
            'monto_subtotal': forms.TextInput(attrs={'placeholder': 'Ejemplo: 50.00'}),
            'fecha_emision': forms.TextInput(attrs={'placeholder': 'Formato: DD/MM/AAAA'}),
            'iva': forms.TextInput(attrs={'placeholder': 'Ejemplo: 4.00'}),
            'monto_total': forms.TextInput(attrs={'placeholder': 'Ejemplo:54.00'}),
        }
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
		self.fields['iva'].label = "IVA"
		self.fields['monto_total'].label = "Monto Total"


# Form para vista de Factura
class EditarFacturaForm(forms.ModelForm):
	
	class Meta:
		model = Factura
		fields = ['monto_subtotal','fecha_emision', 'iva', 'monto_total']

	def __init__(self, *args, **kwargs):
		super(EditarFacturaForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'factura-form'
		self.helper.form_method = 'post'
		self.helper.form_class =  'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['monto_subtotal'].label = "Monto Subtotal"
		self.fields['fecha_emision'].label = "Fecha de emisión"
		self.fields['iva'].label = "IVA"
		self.fields['monto_total'].label = "Monto Total"
		self.helper.layout = Layout(
			'monto_subtotal',
			'fecha_emision',
			'iva',
			'monto_total',
			Div(
                Div(
					HTML("<a href=\"{% url 'autores:postular_trabajo' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),css_class='col-sm-2 col-sm-offset-8'),
                Div(
                	Submit('submit', 'Crear', css_class='btn-success btn-lg btn-block'),css_class='col-sm-2 '),
                css_class="row"),
			
			)
			
