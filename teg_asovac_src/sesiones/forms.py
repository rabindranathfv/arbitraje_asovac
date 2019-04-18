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
        fields = ['nombre_sesion', 'sesion', 'fecha_sesion', 'observaciones', 'fecha_presentacion']

    def __init__(self, *args, **kwargs):
        super(SesionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"
        
        self.fields['nombre_sesion'].label = "Nombre de sesión"
        self.fields['fecha_sesion'].label = "Fecha de sesión"
        self.fields['fecha_presentacion'].label = "Fecha de presentación"   

        self.helper.layout = Layout(
            Div(
                Field('nombre_sesion', placeholder = "Introduzca el nombre de la sesión"),
                Field('sesion', placeholder = "Introduzca la sesión"),
                'fecha_sesion',
                Field('observaciones', rows = "3", placeholder = "Introduzca sus observaciones"),
                'fecha_presentacion',
                css_class = "sesion_form col-sm-6"
            )
        ) 


class EspacioFisicoForm(forms.ModelForm):
    
    class Meta:
        model = Espacio_fisico
        fields = ['nombre', 'capacidad', 'ubicacion', 'video_beam', 'portatil', 'turno']

    def __init__(self, *args, **kwargs):
        super(EspacioFisicoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"

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
        