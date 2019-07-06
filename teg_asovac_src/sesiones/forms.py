# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from .models import Sesion, Espacio_fisico, Espacio_virtual

class SesionForm(forms.ModelForm):
    
    class Meta:
        model = Sesion
        fields = ['nombre_sesion', 'lugar', 'fecha_sesion', 'hora_inicio', 'hora_fin','observaciones', 'capacidad', 'proyector', 'portatil']

    def __init__(self, *args, **kwargs):
        super(SesionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"
        
        self.fields['nombre_sesion'].label = "Nombre de sesión"
        self.fields['fecha_sesion'].label = "Fecha de sesión"
        self.fields['hora_inicio'].label = "Hora de inicio"
        self.fields['hora_fin'].label = "Hora de fin"
        self.fields['portatil'].label = "Portátil"
        self.fields['fecha_sesion'].input_formats = ('%d/%m/%Y',)
        self.fields['hora_inicio'].input_formats = ('%I:%M %p',)
        self.fields['hora_fin'].input_formats = ('%I:%M %p',)
        self.helper.layout = Layout(
            Div(
                Field('nombre_sesion', placeholder = "Introduzca el nombre de la sesión"),
                Field('lugar', placeholder = "Introduzca el lugar"),
                Field('fecha_sesion', placeholder = "Formato: dd/mm/yyyy"),
                Field('hora_inicio', placeholder = "Ejemplo: 8:00 AM"),
                Field('hora_fin', placeholder = "Ejemplo: 12:00 PM"),
                Field('observaciones', rows = "3", placeholder = "Introduzca sus observaciones"),
                'capacidad',
                'proyector',
                'portatil'
            )
        ) 

    def clean_hora_fin(self):
        hora_inicio = self.cleaned_data['hora_inicio']
        hora_fin = self.cleaned_data['hora_fin']
        if hora_inicio > hora_fin:
			raise forms.ValidationError(_("La hora de inicio debe ser antes de la hora de fin."), code = "Horas incorrectas")
        return hora_fin


class EspacioFisicoForm(forms.ModelForm):
    
    class Meta:
        model = Espacio_fisico
        fields = ['nombre', 'capacidad', 'ubicacion', 'video_beam', 'portatil', 'turno']

    def __init__(self, *args, **kwargs):
        super(EspacioFisicoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"

        self.fields['ubicacion'].label = 'Ubicación'
        self.helper.layout = Layout(
            Div(
                Field('nombre', placeholder = "Introduzca el nombre del espacio"),
                Field('capacidad', placeholder = "Introduzca la capacidad"),
                Field('ubicacion', rows="3", placeholder = "Introduzca la ubicación"),
                'video_beam',
                'portatil',
                'turno'
            )
        )

class EspacioVirtualForm(forms.ModelForm):

    class Meta:
        model = Espacio_virtual
        fields =['url_virtual', 'capacidad_url', 'turno']
    
    def __init__(self, *args, **kwargs):
        super(EspacioVirtualForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"

        self.helper.layout = Layout(
            Div(
                Field('url_virtual', placeholder = "Introduzca la URL"),
                Field('capacidad_url', placeholder = "Introduzca la capacidad"),
                Field('turno')
            )
        )
        