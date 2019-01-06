# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from django.core.urlresolvers import reverse

from main_app.models import Sistema_asovac, User
from trabajos.models import Trabajo
from .models import Autor, Datos_pagador, Pago, Factura, Autores_trabajos, Universidad

from django.utils.translation import ugettext_lazy as _ #usado para personalizar las etiquetas de los formularios

#Form para que el autor cree su instancia de autor
class AuthorCreateAutorForm(forms.ModelForm):

	class Meta:
		model = Autor
		fields = ['universidad','genero', 'cedula_pasaporte', 'telefono_oficina', 'telefono_habitacion_celular',
				 'constancia_estudio', 'direccion_envio_correspondencia', 'es_miembro_asovac', 'capitulo_perteneciente', 'nivel_instruccion']
		widgets = {
			'cedula_pasaporte': forms.TextInput(attrs={'placeholder': 'Formato: V para CI y P para pasaporte, seguido del número.'}),
            'direccion_envio_correspondencia': forms.Textarea(attrs={'placeholder': 'Introduzca su direccion aquí',
            														'rows':2 }),
            'telefono_oficina': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5821299999999.'}),
            'telefono_habitacion_celular': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5842499999999.'}),
            'capitulo_perteneciente': forms.TextInput(attrs={'placeholder': 'Ejemplo: Caracas'}),
            'nivel_instruccion': forms.TextInput(attrs={'placeholder': 'Ejemplo:bachiller'}),
        }

        
	def __init__(self, *args, **kwargs):
		super(AuthorCreateAutorForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class =  'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['universidad'].queryset = Universidad.objects.order_by('nombre')
		self.fields['genero'].label = "Género"
		self.fields['cedula_pasaporte'].label = "Cédula/Pasaporte"
		self.fields['telefono_oficina'].label = "Teléfono de oficina"
		self.fields['telefono_habitacion_celular'].label = "Teléfono de habitación/celular"
		self.fields['direccion_envio_correspondencia'].label = "Dirección de envío de correspondencia"
		self.fields['capitulo_perteneciente'].label = "Capítulo perteneciente"
		self.fields['nivel_instruccion'].label = "Nivel de instrucción"

	def clean_cedula_pasaporte(self):
		cedula_pasaporte = self.cleaned_data['cedula_pasaporte']
		if Autor.objects.filter(cedula_pasaporte = cedula_pasaporte).exists():
			raise forms.ValidationError(_("Ya existe un autor con esa cédula o pasaporte."), code = "cedula_pasaporte_duplicado")
		if cedula_pasaporte[0] != 'P' and cedula_pasaporte[0] != 'V':
			raise forms.ValidationError(_("Introduzca el formato correcto, antes del número debe ir 'V' o 'P'."), code = "formato incorrecto")
		if not cedula_pasaporte[1:].isdigit():
			raise forms.ValidationError(_("Introduzca el formato correcto, hay letras donde debería ir el número de cédula o pasaporte."), code = "formato incorrecto")
		return cedula_pasaporte

	def clean_telefono_oficina(self):
		telefono_oficina = self.cleaned_data['telefono_oficina']
		telefono_oficina_length = len(telefono_oficina)
		if telefono_oficina_length < 10 or telefono_oficina_length > 15:
			raise forms.ValidationError(_("Cantidad de dígitos de teléfono de oficina inválido, debe estar entre 10-15 dígitos (Incluyendo código de aŕea del país y operadora)"), code = "telefono_oficina_invalido")
		if not telefono_oficina.isdigit():
			raise forms.ValidationError(_("El teléfono de oficina no puede tener letras ni espacios."), code = "invalid_phone")
		return telefono_oficina

	def clean_telefono_habitacion_celular(self):
		telefono_habitacion_celular = self.cleaned_data['telefono_habitacion_celular']
		telefono_habitacion_celular_length = len(telefono_habitacion_celular)
		if telefono_habitacion_celular_length < 10 or telefono_habitacion_celular_length > 15:
			raise forms.ValidationError(_("Cantidad de dígitos de teléfono de habitacion/celular inválido, debe estar entre 10-15 dígitos (Incluyendo código de aŕea del país y operadora)"), code = "telefono_oficina_invalido")
		if not telefono_habitacion_celular.isdigit():
			raise forms.ValidationError(_("El teléfono de habitación/celular no puede tener letras ni espacios."), code = "invalid_phone")
		return telefono_habitacion_celular







# Form para añadir autores a un trabajo
class AddAuthorToJobForm(forms.ModelForm):

	class Meta:
		model = Autores_trabajos
		fields = ['es_ponente', 'es_coautor']

	correo = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Introduzca el correo electrónico del coautor'}))
	
	def __init__(self, *args, **kwargs):
		self.autor_trabajo = kwargs.pop('autor_trabajo',None)
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
			Div(
				Field('correo',placeholder="Introduzca correo electrónico del coautor"),
				'es_ponente',
				'es_coautor',
				css_class= "row"
				)
			)
	def clean_correo(self):
		correo = self.cleaned_data['correo']
		if not Autor.objects.filter(correo_electronico = correo).exists():
			raise forms.ValidationError(_("No existe algún autor con el correo indicado. Verifique el correo electronico suministrado. En el caso que el coautor no tenga cuenta, debe crearse una y registrarse en la aplicacion de arbitrajes para poder añadirlo como coautor."), code = "email_with_no_user")
		if Autores_trabajos.objects.filter(autor__correo_electronico = correo, trabajo = self.autor_trabajo.trabajo):
			raise forms.ValidationError(_("Ya el autor indicado forma parte de este trabajo."), code = "author_repeated")
		return correo

		
# Form para datos del pagador
class DatosPagadorForm(forms.ModelForm):

	class Meta:
		model = Datos_pagador
		fields = ['categorias_pago','cedula', 'nombres', 'apellidos', 'pasaporte_rif', 'telefono_oficina', 'telefono_habitacion_celular', 'direccion_fiscal']
		widgets = {
            'cedula': forms.TextInput(attrs={'placeholder': 'Ejemplo:12345678'}),
            'nombres': forms.TextInput(attrs={'placeholder': 'Ejemplo: Juan Enrique'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Ejemplo:Carrasco Lopez'}),
            'pasaporte_rif': forms.TextInput(attrs={'placeholder': 'Formato: Jxxxxxxxx o Pxxxxxxxx'}),
            'telefono_oficina': forms.TextInput(attrs={'placeholder': 'Ejemplo: 582129999999'}),
            'telefono_habitacion_celular': forms.TextInput(attrs={'Ejemplo': 'Ejemplo: 584249999999'}),
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

	def clean_cedula(self):
		cedula = self.cleaned_data['cedula']
		if not cedula.isdigit():
			raise forms.ValidationError(_("Introduzca el formato correcto, la cédula debe tener solamente dígitos."), code = "invalid_number")
		return cedula

	def clean_nombres(self):
		nombres=self.cleaned_data['nombres']
		for char in nombres:
			if not char.isalpha() and char !=' ':
				raise forms.ValidationError(_("El nombre debe ser solo letras"), code="invalid_first_name")
		return nombres

	def clean_apellidos(self):
		apellidos=self.cleaned_data['apellidos']
		for char in apellidos:
			if not char.isalpha() and char!= ' ':
				raise forms.ValidationError(_("El apellido debe ser solo letras"), code="invalid_last_name")
		return apellidos

	def clean_pasaporte_rif(self):
		pasaporte_rif = self.cleaned_data['pasaporte_rif']
		if pasaporte_rif:	
			if pasaporte_rif[0] != 'P' and pasaporte_rif[0] != 'J':
				raise forms.ValidationError(_("Introduzca el formato correcto, antes del número debe ir 'J' o 'P'."), code = "formato incorrecto")
			if not pasaporte_rif[1:].isdigit():
				raise forms.ValidationError(_("Introduzca el formato correcto, hay letras donde debería ir el número de rif o pasaporte."), code = "formato incorrecto")
		return pasaporte_rif

	def clean_telefono_oficina(self):
		telefono_oficina = self.cleaned_data['telefono_oficina']
		telefono_oficina_length = len(telefono_oficina)
		if telefono_oficina:	
			if telefono_oficina_length < 10 or telefono_oficina_length > 15:
				raise forms.ValidationError(_("Cantidad de dígitos de teléfono de oficina inválido, debe estar entre 10-15 dígitos (Incluyendo código de aŕea del país y operadora)"), code = "telefono_oficina_invalido")
			if not telefono_oficina.isdigit():
				raise forms.ValidationError(_("El teléfono de oficina no puede tener letras ni espacios."), code = "invalid_phone")
		return telefono_oficina

	def clean_telefono_habitacion_celular(self):
		telefono_habitacion_celular = self.cleaned_data['telefono_habitacion_celular']
		telefono_habitacion_celular_length = len(telefono_habitacion_celular)
		if telefono_habitacion_celular_length < 10 or telefono_habitacion_celular_length > 15:
			raise forms.ValidationError(_("Cantidad de dígitos de teléfono de habitacion/celular inválido, debe estar entre 10-15 dígitos (Incluyendo código de aŕea del país y operadora)"), code = "telefono_oficina_invalido")
		if not telefono_habitacion_celular.isdigit():
			raise forms.ValidationError(_("El teléfono de habitación/celular no puede tener letras ni espacios."), code = "invalid_phone")
		return telefono_habitacion_celular

		

# Form para vista de pago
class PagoForm(forms.ModelForm):

	class Meta:
		model = Pago
		fields = ['tipo_pago', 'numero_cuenta_origen', 'banco_origen', 'numero_transferencia', 'numero_cheque', 'fecha_pago', 'observaciones', 'comprobante_pago']
		widgets = {
            'numero_cuenta_origen': forms.TextInput(attrs={'placeholder': 'Formato: XXXX-XXXX-XXXX-XXXX-XXXX'}),
            'numero_transferencia': forms.TextInput(attrs={'placeholder': 'Formato: XXXXXXXXXX'}),
            'numero_cheque': forms.TextInput(attrs={'placeholder': 'Formato: XXXXXXXXXX'}),
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

	def clean_numero_cuenta_origen(self):
		numero_cuenta_origen = self.cleaned_data['numero_cuenta_origen']
		if(numero_cuenta_origen[4] != '-' or numero_cuenta_origen[9] != '-' or numero_cuenta_origen[14] != '-' or numero_cuenta_origen[19] != '-'):
			raise forms.ValidationError(_("Formato incorrecto, debe ser de la siguiente forma: XXXX-XXXX-XXXX-XXXX-XXXX (incluyendo guiones)"),code="invalid")
		if(not numero_cuenta_origen[:4].isdigit() or not numero_cuenta_origen[5:9].isdigit() or not numero_cuenta_origen[10:14].isdigit() or not numero_cuenta_origen[15:19].isdigit() or not numero_cuenta_origen[20:].isdigit()):
			raise forms.ValidationError(_("El número de cuenta no puede tener letras o espacios."), code="invalid")
		return numero_cuenta_origen

	def clean_numero_transferencia(self):
		numero_transferencia = self.cleaned_data['numero_transferencia']
		if(self.cleaned_data['tipo_pago'] == 'T'):
			if(not numero_transferencia):
				raise forms.ValidationError(_("Falta indicar el número de transferencia, ya que indicó que el tipo de pago es transferencia"),code="required_numero_transferencia")
			else:
				if(numero_transferencia[0] == '0'):
					raise forms.ValidationError(_("El número de transferencia no puede tener 0's a la izquierda."), code="invalid_numero_transferencia")
				if(not numero_transferencia.isdigit()):
					raise forms.ValidationError(_("El número de transferencia no puede contener letras ni espacios."), code="invalid_numero_transferencia")
				if(Pago.objects.filter(numero_transferencia = numero_transferencia).exists()):
					raise forms.ValidationError(_("Ya existe un pago registrado con este número de transferencia"), code = "numero_transferencia_duplicated")
		else:
			if(numero_transferencia):
				raise forms.ValidationError(_("El tipo de pago indicado es CHEQUE, si es correcto por favor deje este campo en blanco."))
		return numero_transferencia

	def clean_numero_cheque(self):
		numero_cheque = self.cleaned_data['numero_cheque']
		if(self.cleaned_data['tipo_pago'] == 'C'):
			if(not numero_cheque):
				raise forms.ValidationError(_("Falta indicar el número de cheque, ya que indicó que el tipo de pago es cheque"),code="required_numero_cheque")
			else:
				if(numero_cheque[0] == '0'):
					raise forms.ValidationError(_("El número de cheque no puede tener 0's a la izquierda."), code="invalid_numero_cheque")
				if(not numero_cheque.isdigit()):
					raise forms.ValidationError(_("El número de cheque no puede contener letras ni espacios."), code="invalid_numero_cheque")
				if(Pago.objects.filter(numero_transferencia = numero_cheque).exists()):
					raise forms.ValidationError(_("Ya existe un pago registrado con este número de cheque"), code = "numero_cheque_duplicated")
		else:
			if(numero_cheque):
				raise forms.ValidationError(_("El tipo de pago indicado es TRANSFERENCIA, si es correcto por favor deje este campo en blanco."))
		return numero_cheque


# Form para vista de Factura
class FacturaForm(forms.ModelForm):
	
	class Meta:
		model = Factura
		fields = ['fecha_emision', 'monto_total']
		widgets = {
            'fecha_emision': forms.TextInput(attrs={'placeholder': 'Formato: DD/MM/AAAA'}),
        }
	def __init__(self, *args, **kwargs):
		super(FacturaForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.fields['monto_total'].widget.attrs['placeholder'] = 'Ejemplo: 100.50'
		self.helper.form_id = 'factura-form'
		self.helper.form_method = 'post'
		self.helper.form_class =  'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['fecha_emision'].label = "Fecha de emisión"
		self.fields['monto_total'].label = "Monto Total"

	def clean_monto_total(self):
		monto_total = self.cleaned_data['monto_total']
		if monto_total <= 0:
			raise forms.ValidationError(_("El monto debe ser mayor que 0."),code = "invalid_monto_total")
		return monto_total

#Form para que el admin o coordinador general cree un autor
class AdminCreateAutorForm(forms.ModelForm):

	class Meta:
		model = Autor
		fields = ['universidad','nombres', 'apellidos', 'genero', 'cedula_pasaporte', 'correo_electronico', 'telefono_oficina', 'telefono_habitacion_celular', 'constancia_estudio', 'direccion_envio_correspondencia', 'es_miembro_asovac', 'capitulo_perteneciente', 'nivel_instruccion','observaciones']
		widgets = {
			'nombres': forms.TextInput(attrs={'placeholder': 'Ejemplo:Juan Enrique'}),
			'apellidos': forms.TextInput(attrs={'placeholder': 'Ejemplo:Castro Rodriguez'}),
			'cedula_pasaporte': forms.TextInput(attrs={'placeholder': 'Formato: V para CI y P para pasaporte, seguido del número.'}),
            'direccion_envio_correspondencia': forms.Textarea(attrs={'placeholder': 'Introduzca su direccion aquí',
            														'rows':2 }),
            'correo_electronico': forms.TextInput(attrs={'placeholder': 'Ejemplo: juancastro@gmail.com'}),
            'telefono_oficina': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5821299999999. Debe incluir el código de area y de operadora, no es necesario el "+"'}),
            'telefono_habitacion_celular': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5842499999999. Debe incluir el código de area y de operadora, no es necesario el "+"'}),
            'capitulo_perteneciente': forms.TextInput(attrs={'placeholder': 'Ejemplo: Caracas'}),
            'nivel_instruccion': forms.TextInput(attrs={'placeholder': 'Ejemplo:bachiller'}),
            'observaciones': forms.Textarea(attrs={'placeholder': 'Introduzca su observación aquí',
            														'rows':2 })
        }

	def __init__(self, *args, **kwargs):
		super(AdminCreateAutorForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class =  'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['universidad'].queryset = Universidad.objects.order_by('nombre')
		self.fields['genero'].label = "Género"
		self.fields['cedula_pasaporte'].label = "Cédula/Pasaporte"
		self.fields['correo_electronico'].label = "Correo Electrónico"
		self.fields['telefono_oficina'].label = "Teléfono de oficina"
		self.fields['telefono_habitacion_celular'].label = "Teléfono de habitación/celular"
		self.fields['direccion_envio_correspondencia'].label = "Dirección de envío de correspondencia"
		self.fields['capitulo_perteneciente'].label = "Capítulo perteneciente"
		self.fields['nivel_instruccion'].label = "Nivel de instrucción"
		self.helper.layout = Layout(
			Div(
				'universidad',
				Field('nombres',placeholder="Ejemplo: Juanito José"),
				Field('apellidos',placeholder="Ejemplo: Pérez Jiménez"),
				Field('genero',placeholder="Masculino o Femenino"),
				Field('cedula_pasaporte',placeholder="Formato: V para CI y P para pasaporte, seguido del número."),
				Field('correo_electronico',placeholder="Ejemplo: Juanito@servidor.com"),
				Field('telefono_oficina',placeholder="Ejemplo: 584249999999"),
				Field('telefono_habitacion_celular',placeholder="Ejemplo: 582129999999"),
				Field('constancia_estudio',placeholder=""),
				Field('direccion_envio_correspondencia',rows='2', placeholder="Ejemplo: Sabana grande, CC El Recreo"),
				'es_miembro_asovac',
				Field('capitulo_perteneciente',placeholder="Ejemplo: Caracas"),
				Field('nivel_instruccion',placeholder="Ejemplo: Bachiller"),
				Field('observaciones',rows='2', placeholder="Introduzca sus observaciones aquí"),
				Div(
	                Div(
	                    HTML("<a href=\"{% url 'autores:authors_list' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
	                css_class='col-sm-offset-7 col-sm-2'),
	                Div(
	                    Submit('submit', 'Crear autor', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
	                css_class='col-sm-2'),
	                css_class='row')
	       		 )
			)
	
	def clean_nombres(self):
		nombres=self.cleaned_data['nombres']
		for char in nombres:
			if not char.isalpha() and char !=' ':
				raise forms.ValidationError(_("El nombre debe ser solo letras"), code="invalid_first_name")
		return nombres

	def clean_apellidos(self):
		apellidos=self.cleaned_data['apellidos']
		for char in apellidos:
			if not char.isalpha() and char!= ' ':
				raise forms.ValidationError(_("El apellido debe ser solo letras"), code="invalid_last_name")
		return apellidos

	def clean_correo_electronico(self):
		correo_electronico = self.cleaned_data['correo_electronico']
		# Si el email ya esta en uso, levantamos un error.
		if User.objects.filter(email=correo_electronico).exists():
			raise forms.ValidationError(_("Dirección de correo ya está en uso, por favor escoja otra."),code="invalid")
		return correo_electronico

	def clean_cedula_pasaporte(self):
		cedula_pasaporte = self.cleaned_data['cedula_pasaporte']
		if Autor.objects.filter(cedula_pasaporte = cedula_pasaporte).exists():
			raise forms.ValidationError(_("Ya existe un autor con esa cédula o pasaporte."), code = "cedula_pasaporte_duplicado")
		if cedula_pasaporte[0] != 'P' and cedula_pasaporte[0] != 'V':
			raise forms.ValidationError(_("Introduzca el formato correcto, antes del número debe ir 'V' o 'P'."), code = "formato incorrecto")
		if not cedula_pasaporte[1:].isdigit():
			raise forms.ValidationError(_("Introduzca el formato correcto, hay letras donde debería ir el número de cédula o pasaporte."), code = "formato incorrecto")
		return cedula_pasaporte

	def clean_telefono_oficina(self):
		telefono_oficina = self.cleaned_data['telefono_oficina']
		telefono_oficina_length = len(telefono_oficina)
		if telefono_oficina_length < 10 or telefono_oficina_length > 15:
			raise forms.ValidationError(_("Cantidad de dígitos de teléfono de oficina inválido, debe estar entre 10-15 dígitos (Incluyendo código de aŕea del país y operadora)"), code = "telefono_oficina_invalido")
		if not telefono_oficina.isdigit():
			raise forms.ValidationError(_("El teléfono de oficina no puede tener letras ni espacios."), code = "invalid_phone")
		return telefono_oficina

	def clean_telefono_habitacion_celular(self):
		telefono_habitacion_celular = self.cleaned_data['telefono_habitacion_celular']
		telefono_habitacion_celular_length = len(telefono_habitacion_celular)
		if telefono_habitacion_celular_length < 10 or telefono_habitacion_celular_length > 15:
			raise forms.ValidationError(_("Cantidad de dígitos de teléfono de habitacion/celular inválido, debe estar entre 10-15 dígitos (Incluyendo código de aŕea del país y operadora)"), code = "telefono_oficina_invalido")
		if not telefono_habitacion_celular.isdigit():
			raise forms.ValidationError(_("El teléfono de habitación/celular no puede tener letras ni espacios."), code = "invalid_phone")
		return telefono_habitacion_celular


#Form para que el admin o coordinador general cree un autor
class EditAutorForm(forms.ModelForm):

	class Meta:
		model = Autor
		fields = ['universidad', 'nombres', 'apellidos', 'genero', 'cedula_pasaporte', 'correo_electronico', 'telefono_oficina', 'telefono_habitacion_celular', 'constancia_estudio', 'direccion_envio_correspondencia', 'es_miembro_asovac', 'capitulo_perteneciente', 'nivel_instruccion','observaciones']
		widgets = {
			'nombres': forms.TextInput(attrs={'placeholder': 'Ejemplo:Juan Enrique'}),
			'apellidos': forms.TextInput(attrs={'placeholder': 'Ejemplo:Castro Rodriguez'}),
			'cedula_pasaporte': forms.TextInput(attrs={'placeholder': 'Formato: V para CI y P para pasaporte, seguido del número.'}),
            'direccion_envio_correspondencia': forms.Textarea(attrs={'placeholder': 'Introduzca su direccion aquí',
            														'rows':2 }),
            'correo_electronico': forms.TextInput(attrs={'placeholder': 'Ejemplo: juancastro@gmail.com'}),
            'telefono_oficina': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5821299999999.'}),
            'telefono_habitacion_celular': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5842499999999.'}),
            'capitulo_perteneciente': forms.TextInput(attrs={'placeholder': 'Ejemplo: Caracas'}),
            'nivel_instruccion': forms.TextInput(attrs={'placeholder': 'Ejemplo:bachiller'}),
            'observaciones': forms.Textarea(attrs={'placeholder': 'Introduzca su observación aquí',
            														'rows':2 })
        }
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user',None)
		super(EditAutorForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_class =  'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['universidad'].queryset = Universidad.objects.order_by('nombre')
		self.fields['genero'].label = "Género"
		self.fields['cedula_pasaporte'].label = "Cédula/Pasaporte"
		self.fields['correo_electronico'].label = "Correo Electrónico"
		self.fields['telefono_oficina'].label = "Teléfono de oficina"
		self.fields['telefono_habitacion_celular'].label = "Teléfono de habitación/celular"
		self.fields['direccion_envio_correspondencia'].label = "Dirección de envío de correspondencia"
		self.fields['capitulo_perteneciente'].label = "Capítulo perteneciente"
		self.fields['nivel_instruccion'].label = "Nivel de instrucción"
		self.helper.layout = Layout(
			Div(
				'universidad',
				Field('nombres',placeholder="Ejemplo: Juanito José"),
				Field('apellidos',placeholder="Ejemplo: Pérez Jiménez"),
				Field('genero',placeholder="Masculino o Femenino"),
				Field('cedula_pasaporte',placeholder="Formato: Vxxxxxxxx o Pxxxxxxxx. V para cédula venezolana o P para pasaporte."),
				Field('correo_electronico',placeholder="Ejemplo: Juanito@servidor.com"),
				Field('telefono_oficina',placeholder="Ejemplo: 584249999999"),
				Field('telefono_habitacion_celular',placeholder="Ejemplo: 582129999999"),
				Field('constancia_estudio',placeholder=""),
				Field('direccion_envio_correspondencia',placeholder="Ejemplo: Sabana grande, CC El Recreo"),
				'es_miembro_asovac',
				Field('capitulo_perteneciente',placeholder="Ejemplo: Caracas"),
				Field('nivel_instruccion',placeholder="Ejemplo: Bachiller"),
				Field('observaciones',placeholder="Introduzca sus observaciones aquí", rows="2"),
				Div(
	                Div(
	                    HTML("<a href=\"{% url 'autores:authors_list' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
	                css_class='col-sm-offset-7 col-sm-2'),
	                Div(
	                    Submit('submit', 'Editar autor', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
	                css_class='col-sm-2'),
	                css_class='row')
	       		 )
			)

	def clean_nombres(self):
		nombres=self.cleaned_data['nombres']
		for char in nombres:
			if not char.isalpha() and char !=' ':
				raise forms.ValidationError(_("El nombre debe ser solo letras"), code="invalid_first_name")
		return nombres

	def clean_apellidos(self):
		apellidos=self.cleaned_data['apellidos']
		for char in apellidos:
			if not char.isalpha() and char!= ' ':
				raise forms.ValidationError(_("El apellido debe ser solo letras"), code="invalid_last_name")
		return apellidos

	def clean_correo_electronico(self):
		correo_electronico = self.cleaned_data['correo_electronico']
		# Si el email ya esta en uso, levantamos un error.

		if User.objects.filter(email=correo_electronico).exists() and self.user.email != correo_electronico:
			raise forms.ValidationError(_("Dirección de correo ya está registrada con otro usuario, por favor escoja otra."),code="invalid")
		return correo_electronico

	def clean_cedula_pasaporte(self):
		cedula_pasaporte = self.cleaned_data['cedula_pasaporte']
		autor = Autor.objects.get(usuario__usuario = self.user)
		if Autor.objects.filter(cedula_pasaporte = cedula_pasaporte).exists() and autor.cedula_pasaporte != cedula_pasaporte:
			raise forms.ValidationError(_("Ya existe un autor con esa cédula o pasaporte."), code = "cedula_pasaporte_duplicado")
		if cedula_pasaporte[0] != 'P' and cedula_pasaporte[0] != 'V':
			raise forms.ValidationError(_("Introduzca el formato correcto, antes del número debe ir 'V' o 'P'."), code = "formato incorrecto")
		if not cedula_pasaporte[1:].isdigit():
			raise forms.ValidationError(_("Introduzca el formato correcto, hay letras donde debería ir el número de cédula o pasaporte."), code = "formato incorrecto")
		return cedula_pasaporte

	def clean_telefono_oficina(self):
		telefono_oficina = self.cleaned_data['telefono_oficina']
		telefono_oficina_length = len(telefono_oficina)
		if telefono_oficina_length < 10 or telefono_oficina_length > 15:
			raise forms.ValidationError(_("Cantidad de dígitos de teléfono de oficina inválido, debe estar entre 10-15 dígitos (Incluyendo código de aŕea del país y operadora)"), code = "telefono_oficina_invalido")
		if not telefono_oficina.isdigit():
			raise forms.ValidationError(_("El teléfono de oficina no puede tener letras ni espacios."), code = "invalid_phone")
		return telefono_oficina

	def clean_telefono_habitacion_celular(self):
		telefono_habitacion_celular = self.cleaned_data['telefono_habitacion_celular']
		telefono_habitacion_celular_length = len(telefono_habitacion_celular)
		if telefono_habitacion_celular_length < 10 or telefono_habitacion_celular_length > 15:
			raise forms.ValidationError(_("Cantidad de dígitos de teléfono de habitacion/celular inválido, debe estar entre 10-15 dígitos (Incluyendo código de aŕea del país y operadora)"), code = "telefono_oficina_invalido")
		if not telefono_habitacion_celular.isdigit():
			raise forms.ValidationError(_("El teléfono de habitación/celular no puede tener letras ni espacios."), code = "invalid_phone")
		return telefono_habitacion_celular