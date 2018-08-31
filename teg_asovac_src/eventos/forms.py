# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions,InlineRadios
from django import forms
from django.core.urlresolvers import reverse
from django.core.validators import EmailValidator,URLValidator

from eventos.validators import validate_ced_passport,validate_phone_office,validate_phone_personal,validate_cap_asovac 
from eventos.models import Organizador,Evento,Locacion_evento,Organizador_evento


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
        self.fields['institucion'].label = "Institución"
        self.fields['telefono_oficina'].label = "Teléfono de Oficina"
        self.fields['telefono_habitacion_celular'].label = "Teléfono Habitacion/Celular"
        self.fields['direccion_correspondencia'].label = "Dirección"
        self.fields['es_miembro_asovac'].label = "Es Mienbro de AsoVAC"
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
            #Field('usuario_asovac', type="hidden"),
            'usuario_asovac',
            Div(
                Div(
                    HTML("<span></span>"),
                css_class='col-sm-7'),

                Div(
                    HTML("<a href=\"{% url 'eventos:organizer_create' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
                css_class='col-sm-2'),

                Div(
                    Submit('submit', 'Agregar Organizador', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
                css_class='col-sm-3'),

                # Div(
                #     HTML("<a href=\"#\" class=\"btn btn-info btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#modal-success\">Ver</a>"),
                # css_class='col-sm-1'),

            css_class='col-sm-12')
        )
    def clean_names(self):
        names_data = self.cleaned_data['nombres']
        return names_data
    
    def clean_lastnames(self):
        lastnames_data = self.cleaned_data['apellidos']
        return lastnames_data
    
    def clean_gender(self):
        gender_data = self.cleaned_data['genero']
        return gender_data

    def clean_cedula_pass(self):
        cedula_pass_data = self.cleaned_data['cedula_o_pasaporte']
        return cedula_pass_data

    def clean_email(self):
        email_data = self.cleaned_data['correo_electronico']
        return email_data

    def clean_institution(self):
        institution_data = self.cleaned_data['institucion']
        return institution_data

    def clean_phone_office(self):
        phone_office_data = self.cleaned_data['telefono_oficina']
        return phone_office_data

    def clean_phone_personal(self):
        phone_personal_data = self.cleaned_data['telefono_habitacion_celular']
        return phone_personal_data

    def clean_address(self):
        address_data = self.cleaned_data['direccion_correspondencia']
        return address_data

    def clean_asovac_menber(self):
        asovac_menber_data = self.cleaned_data['es_miembro_asovac']
        return asovac_menber_data

    def clean_cap_asovac(self):
        capitulo_asovac_data = self.cleaned_data['capitulo_asovac']       
        return capitulo_asovac_data

    def clean_position_institution(self):
        cargo_institucion_data = self.cleaned_data['cargo_en_institucion']
        return cargo_institucion_data

    def clean_url_organizer(self):
        url_organizador_data = self.cleaned_data['url_organizador']
        return url_organizador_data

    def clean_observations(self):
        observaciones_data = self.cleaned_data['observaciones'] 
        return observaciones_data

    def clean_user_asovac(self):
        user_asovac_data = self.cleaned_data['usuario_asovac']
        return user_asovac_data
    
class CreateEventForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        fields = ['nombre','categoria', 'descripcion', 'tipo','fecha_inicio','fecha_fin','dia_asignado',
        'duracion','horario_preferido','fecha_preferida','observaciones','url_anuncio_evento',
        'organizador_id','locacion_evento']

    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'create-event-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-8'
        self.fields['nombre'].label = 'Nombre del Evento'
        self.fields['categoria'].label = 'Categoria del Evento'
        self.fields['descripcion'].label = 'Descripción'
        self.fields['tipo'].label = 'Tipo de Evento'
        self.fields['fecha_inicio'].label = 'Fecha de Inicio'
        self.fields['fecha_fin'].label = 'Fecha de Finalizacion'
        self.fields['dia_asignado'].label = 'Dia Asignado'
        self.fields['duracion'].label = 'Duracion del Evento'
        self.fields['horario_preferido'].label = 'Horario Preferido'
        self.fields['fecha_preferida'].label = 'Fecha Preferida'
        self.fields['observaciones'].label = 'Observaciones'
        self.fields['url_anuncio_evento'].label = 'Enlace del Evento'
        self.fields['organizador_id'].label = 'Organizador ID'
        self.fields['locacion_evento'].label = 'Locacizacion del Evento'
        #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
        #self.helper.add_input(Submit('submit', 'Crear', css_class='btn-success btn-lg pull-right'))
        self.helper.layout = Layout( # the order of the items in this layout is important
            'nombre',
            'categoria',
            'descripcion',
            'tipo',
            'fecha_inicio',
            'fecha_fin',
            'dia_asignado',
            'duracion',
            'horario_preferido',
            'fecha_preferida',
            'observaciones',
            'url_anuncio_evento',
            'organizador_id',
            'locacion_evento',
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
