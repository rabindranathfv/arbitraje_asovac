# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from django.core.urlresolvers import reverse

from .models import Organizador,Evento,Locacion_evento,Organizador_evento

# class MyLoginForm(forms.Form):
#     username = forms.CharField(label="Usuario", max_length=100)
#     password = forms.CharField(label="Contraseña", max_length=100, widget=forms.PasswordInput)

#     def __init__(self, *args, **kwargs):
#        super(MyLoginForm, self).__init__(*args, **kwargs)
#        self.helper = FormHelper()
#        self.helper.form_id = 'login-form'
#        self.helper.form_method = 'post'
#        #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
#        self.helper.add_input(Submit('submit', 'Ingresar', css_class='btn-block'))

# class DataBasicForm(forms.Form):
#     name_arbitration= forms.CharField(label="Nombre arbitraje", max_length=20)
#     description= forms.CharField(label="Descripción", max_length=255)
#     start_date= forms.DateField(label="Fecha de inicio")
#     end_date= forms.DateField(label="Fecha de fin")
        
        # super(MyLoginForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_id = 'login-form'
        # self.helper.form_method = 'post'
        # #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
        # self.helper.add_input(Submit('submit', 'Ingresar', css_class='btn-block'))

class CreateOrganizerForm(forms.ModelForm):

    class Meta:
        model = Organizador
        fields = ['nombres','apellidos', 'genero','cedula_o_pasaporte', 'correo_electronico','institucion',
                'telefono_oficina','telefono_habitacion_celular','direccion_correspondencia',
                'es_miembro_asovac','capitulo_asovac','cargo_en_institucion','url_organizador',
                'observaciones','usuario_asovac']

    def __init__(self, *args, **kwargs):
        super(CreateOrganizerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'create-organizer-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-8'
        self.fields['nombres'].label = "Nombres"
        self.fields['apellidos'].label = "Apellidos"
        self.fields['genero'].label = "Genero"
        self.fields['cedula_o_pasaporte'].label = "Cédula o Pasaporte"
        self.fields['correo_electronico'].label = "Correo Electronico"
        self.fields['institucion'].label = "Institucirón"
        self.fields['telefono_oficina'].label = "Teléfono de Oficina"
        self.fields['telefono_habitacion_celular'].label = "Teléfono Habitacion/Celular"
        self.fields['direccion_correspondencia'].label = "Dirección"
        self.fields['es_miembro_asovac'].label = ""
        self.fields['capitulo_asovac'].label = "Capitulo AsoVAC"
        self.fields['cargo_en_institucion'].label = "Cargo en la Institución"
        self.fields['url_organizador'].label = "Enlace del Organizador"
        self.fields['observaciones'].label = "Observaciones"
        self.fields['usuario_asovac'].label = "Usuario"
        
        #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
        #self.helper.add_input(Submit('submit', 'Crear', css_class='btn-success btn-lg pull-right'))
        self.helper.layout = Layout( # the order of the items in this layout is important
            'nombres',
            'apellidos',
            'genero',
            'cedula_o_pasaporte',
            'correo_electronico',
            'institucion',
            'telefono_oficina',
            'telefono_habitacion_celular',
            'direccion_correspondencia',
            'es_miembro_asovac',
            'capitulo_asovac',
            'cargo_en_institucion',
            'url_organizador',
            'observaciones',
            'usuario_asovac',
            Div(
                Div(
                    HTML("<span></span>"),
                css_class='col-sm-7'),

                Div(
                    HTML("<a href=\"{% url 'eventos:organizer_create' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
                css_class='col-sm-2'),

                Div(
                    Submit('submit', 'Agregar Organizador', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success', action="/eventos/listar-organizadores/"),
                css_class='col-sm-3'),

                # Div(
                #     HTML("<a href=\"#\" class=\"btn btn-info btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#modal-success\">Ver</a>"),
                # css_class='col-sm-1'),

            css_class='col-sm-12')
        )

class CreateEventForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        fields = ['nombre','categoria', 'descripcion', 'tipo','fecha_inicio','fecha_fin','dia_asignado','duracion','horario_preferido','fecha_preferida','observaciones','url_anuncio_evento']

    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'create-event-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-8'
        #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
        #self.helper.add_input(Submit('submit', 'Crear', css_class='btn-success btn-lg pull-right'))
        self.helper.layout = Layout( # the order of the items in this layout is important
            Field('nombre'),
            Field('categoria'),
            Field('descripcion'),
            Field('tipo'),
            Field('fecha_inicio'),
            Field('fecha_fin'),
            Field('dia_asignado'),
            Field('duracion'),
            Field('horario_preferido'),
            Field('fecha_preferida'),
            Field('observaciones'),
            Div(
                Div(
                    HTML("<span></span>"),
                css_class='col-sm-7'),

                Div(
                    HTML("<a href=\"{% url 'eventos:event_create' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
                css_class='col-sm-2'),

                Div(
                    Submit('submit', 'Crear Evento', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
                css_class='col-sm-3'),

                # Div(
                #     HTML("<a href=\"#\" class=\"btn btn-info btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#modal-success\">Ver</a>"),
                # css_class='col-sm-1'),

            css_class='col-sm-12')
        )
