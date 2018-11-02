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
        self.fields['usuario_asovac'].required = False
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
            Field('usuario_asovac', type="hidden"),
            #'usuario_asovac',
            Div(
                Div(
                    HTML("<a href=\"{% url 'eventos:organizer_list' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
                css_class='col-sm-offset-7 col-sm-2'),

                Div(
                    Submit('submit', 'Crear Organizador', css_class='btn-success btn-lg btn-block'),
                css_class='col-sm-3'),
            css_class='row')
        )
    


class CreateEventForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        fields = ['nombre','categoria', 'descripcion', 'tipo','fecha_inicio','fecha_fin','dia_asignado',
        'duracion','horario_preferido','fecha_preferida','observaciones','url_anuncio_evento','locacion_evento']
    email_organizador = forms.EmailField()
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
        self.fields['locacion_evento'].label = 'Localizacion del Evento'
        
        #Helper 1 para crear evento
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
            Field('tipo', placeholder="Ejemplo: Recreacional"),
            Field('fecha_inicio', placeholder="Formato: DD/MM/AAAA"),
            Field('fecha_fin', placeholder="Formato: DD/MM/AAAA"),
            Field('dia_asignado', placeholder="Formato: DD/MM/AAAA"),
            Field('duracion', placeholder="Ejemplo: 1 mes"),
            Field('horario_preferido', placeholder="Ejemplo: Diurno"),
            Field('fecha_preferida', placeholder="Formato: DD/MM/AAAA"),
            Field('email_organizador', placeholder="Ejemplo: juanito_perez123@gmail.com"),
            Field('locacion_preferida', placeholder="Ejemplo: Caracas"),
            Field('observaciones', placeholder="Introduzca sus observaciones aquí"),
            Field('url_anuncio_evento',placeholder="Ejemplo:https://www.reddit.com/"),
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




class EditEventForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        fields = ['nombre','categoria', 'descripcion', 'tipo','fecha_inicio','fecha_fin','dia_asignado',
        'duracion','horario_preferido','fecha_preferida','observaciones','url_anuncio_evento','locacion_evento']

    def __init__(self, *args, **kwargs):
        super(EditEventForm, self).__init__(*args, **kwargs)
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
        self.fields['locacion_evento'].label = 'Localizacion del Evento'
        
        #Helper para editar evento
        self.helper = FormHelper()
        self.helper.form_id = 'edit-event-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-8'
        #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
        #self.helper.add_input(Submit('submit', 'Crear', css_class='btn-success btn-lg pull-right'))
        self.helper.layout = Layout( # the order of the items in this layout is important
            Field('nombre', placeholder="Ejemplo: Asovac 2018"),
            Field('categoria', placeholder="Ejemplo: Fisica"),
            Field('descripcion', placeholder="Introduzca su descripción aquí"),
            Field('tipo', placeholder="Ejemplo: Recreacional"),
            Field('fecha_inicio', placeholder="Formato: DD/MM/AAAA"),
            Field('fecha_fin', placeholder="Formato: DD/MM/AAAA"),
            Field('dia_asignado', placeholder="Formato: DD/MM/AAAA"),
            Field('duracion', placeholder="Ejemplo: 1 mes"),
            Field('horario_preferido', placeholder="Ejemplo: Diurno"),
            Field('fecha_preferida', placeholder="Formato: DD/MM/AAAA"),
            Field('observaciones', placeholder="Introduzca sus observaciones aquí"),
            Field('url_anuncio_evento',placeholder="Ejemplo:https://www.reddit.com/"),
            'locacion_evento',
            Div(
                Div(
                    HTML("<a href=\"{% url 'eventos:event_list' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
                css_class='col-sm-offset-7 col-sm-2'),
                Div(
                    Submit('submit', 'Editar Evento', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
                css_class='col-sm-3'),
                css_class='row')
        )



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
        self.helper.layout = Layout(
            'lugar',
            'descripcion',
            'capacidad_de_asistentes',
            'observaciones',
            'equipo_requerido',
            Div(
                Div(
                    HTML("<a href=\"{% url 'eventos:event_place_list' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
                css_class='col-sm-offset-6 col-sm-2'),

                Div(
                    Submit('submit', 'Crear Locacion de Eventos ', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
                css_class='col-sm-4'),
            css_class='row')
        )



class AddOrganizerToEventForm(forms.Form):
    correo_electronico = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Introduzca el correo electrónico del organizador'}))
    locacion_preferida = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Caracas'}))

    def __init__(self, *args, **kwargs):
        super(AddOrganizerToEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-organizer-to-event-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-7'
        self.fields['correo_electronico'].label = "Correo electrónico del organizador"
        self.fields['locacion_preferida'].label = "Lugar preferido"


class AddObservationsForm(forms.Form):
    observaciones = forms.CharField(max_length = 400, widget=forms.Textarea(attrs={'placeholder': 'Introduzca su observación aquí.'}))
    def __init__(self, *args, **kwargs):
        super(AddObservationsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'add-observation-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-7'
