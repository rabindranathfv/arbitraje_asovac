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
                    Submit('submit', 'Crear Organizador', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
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

    locacion_preferida = forms.CharField(max_length=50)
    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
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
        self.fields['organizador_id'].label = 'Seleccione el Organizador'
        self.fields['locacion_evento'].label = 'Localizacion del Evento'
        
        self.helper1 = FormHelper()
        self.helper1.form_id = 'create-event-form'
        self.helper1.form_method = 'post'
        self.helper1.form_class = 'form-horizontal'
        self.helper1.label_class = 'col-sm-3'
        self.helper1.field_class = 'col-sm-8'
        #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
        #self.helper.add_input(Submit('submit', 'Crear', css_class='btn-success btn-lg pull-right'))
        self.helper1.layout = Layout( # the order of the items in this layout is important
            Field('nombre', placeholder="Ejemplo: Asovac 2018"),
            Field('categoria', placeholder="Ejemplo: Fisica"),
            Field('descripcion', placeholder="Introduzca su descripción aquí"),
            Field('fecha_inicio', placeholder="Formato: DD/MM/AAAA"),
            Field('fecha_fin', placeholder="Formato: DD/MM/AAAA"),
            Field('dia_asignado', placeholder="Formato: DD/MM/AAAA"),
            Field('duracion', placeholder="Ejemplo: 1 mes"),
            Field('horario_preferido', placeholder="Ejemplo: Diurno"),
            Field('fecha_preferida', placeholder="Formato: DD/MM/AAAA"),
            Field('locacion_preferida', placeholder="Ejemplo: Caracas"),
            Field('observaciones', placeholder="Introduzca sus observaciones aquí"),
            'url_anuncio_evento',
            'organizador_id',
            'locacion_evento',
            Div(
                Div(
                    HTML("<a href=\"{% url 'eventos:event_list' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
                css_class='col-sm-offset-7 col-sm-2'),
                Div(
                    Submit('submit', 'Crear Evento', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
                css_class='col-sm-3'),
                css_class='row')
        )

    def clean_name(self):
        name_data = self.cleaned_data['nombre']
        return name_data
    
    def clean_category(self):
        category_data = self.cleaned_data['categoria']
        return category_data
    
    def clean_description(self):
        desription_data = self.cleaned_data['descripcion']
        return desription_data

    def clean_type(self):
        type_data = self.cleaned_data['tipo']
        return type_data

    def clean_start_date(self):
        start_date_data = self.cleaned_data['fecha_inicio']
        return start_date_data

    def clean_end_date(self):
        end_date_data = self.cleaned_data['fecha_fin']
        return end_date_data

    def clean_day(self):
        day_data = self.cleaned_data['dia_asignado']
        return day_data

    def clean_duration(self):
        duration_data = self.cleaned_data['duracion']
        return duration_data

    def clean_preffer_hour(self):
        preffer_hour_data = self.cleaned_data['horario_preferido']
        return preffer_hour_data

    def clean_preffer_date(self):
        preffer_date_data = self.cleaned_data['fecha_preferida']
        return preffer_date_data

    def clean_observations(self):
        observations_data = self.cleaned_data['observaciones']       
        return observations_data

    def clean_url_event(self):
        url_event_data = self.cleaned_data['url_anuncio_evento']
        return url_event_data

    def clean_organizer_id(self):
        organizer_id_data = self.cleaned_data['organizador_id']
        return organizer_id_data

    def clean_locacion_evento(self):
        locacion_event_data = self.cleaned_data['locacion_evento'] 
        return locacion_event_data


class CreateLocacionForm(forms.ModelForm):

    class Meta:
        model = Locacion_evento
        fields = ['lugar','descripcion','capacidad_de_asistentes','observaciones','equipo_requerido']

    def __init__(self, *args, **kwargs):
        super(CreateLocacionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'create-locacion-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-7'
        self.fields['lugar'].label = "Lugar"
        self.fields['descripcion'].label = "Descripción"
        self.fields['capacidad_de_asistentes'].label = "Capacidad de Asistentes"
        self.fields['observaciones'].label = "Observaciones"
        self.fields['equipo_requerido'].label = "Equipo Requerido"
        #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
        #self.helper.add_input(Submit('submit', 'Crear', css_class='btn-success btn-lg pull-right'))
        self.helper.layout = Layout( # the order of the items in this layout is important
            #Field('lugar',readonly=True),
            'lugar',
            'descripcion',
            'capacidad_de_asistentes',
            'observaciones',
            'equipo_requerido',
            Div(
                Div(
                    HTML("<span></span>"),
                css_class='col-sm-6'),

                Div(
                    HTML("<a href=\"{% url 'eventos:event_place_create' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
                css_class='col-sm-2'),

                Div(
                    Submit('submit', 'Crear Locacion de Eventos ', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
                css_class='col-sm-4'),

                # Div(
                #     HTML("<a href=\"#\" class=\"btn btn-info btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#modal-success\">Ver</a>"),
                # css_class='col-sm-1'),

            css_class='col-sm-12')
        )
    def can_udpate_location(self, locacion_id):
        
        return True

    def clean_place(self):
        place_data = self.cleaned_data['lugar']
        return place_data
    
    def clean_description(self):
        description_data = self.cleaned_data['descripcion']
        return description_data
    
    def clean_capacity(self):
        capacity_data = self.cleaned_data['capacidad_de_asistentes']
        return capacity_data

    def clean_observations(self):
        observations_data = self.cleaned_data['observaciones']
        return observations_data

    def clean_equipement(self):
        equipement_data = self.cleaned_data['equipo_requerido']
        return equipement_data