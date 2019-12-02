# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML, Row, Column

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from arbitrajes.models import Arbitro
from autores.models import Autores_trabajos
from main_app.models import Usuario_asovac, Usuario_rol_in_sistema, Sistema_asovac


class CertificateToRefereeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.sistema_id = kwargs.pop('sistema_id')
        super(CertificateToRefereeForm, self).__init__(*args, **kwargs)
        usuarios_arbitros_in_sistema = Usuario_rol_in_sistema.objects.filter(
            rol=4,
            sistema_asovac=self.sistema_id,
            status=True
        )
        arbitros = []
        for usuario_arbitro_in_sistema in usuarios_arbitros_in_sistema:
            arbitro = Arbitro.objects.get(usuario=usuario_arbitro_in_sistema.usuario_asovac)
            arbitros.append((arbitro.id, arbitro.nombres))
        self.fields['arbitros'] = forms.MultipleChoiceField(
            choices=arbitros,
            required=True,
            label="",
            widget=FilteredSelectMultiple("Arbitros", is_stacked=False)
        )


class MultipleRecipientsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(MultipleRecipientsForm, self).__init__(*args, **kwargs)
        # create a new recipients_name blank field
        field1_name = 'recipients_name_0'
        self.fields[field1_name] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={'placeholder':'Nombre completo',
                                          'class':'form-control new-list-item'})
        )
        # create a new recipients_email blank field
        field2_name = 'recipients_email_0'
        self.fields[field2_name] = forms.EmailField(
            required=False,
            widget=forms.EmailInput(attrs={'placeholder':'Correo Electrónico',
                                           'class':'form-control new-list-item'})
        )

    def get_name_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_name_'):
                yield self[field_name]

    def get_email_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_email_'):
                yield self[field_name]


class CertificateToAuthorsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.sistema_id = kwargs.pop('sistema_id')
        super(CertificateToAuthorsForm,self).__init__(*args, **kwargs)
        autores_trabajos = Autores_trabajos.objects.filter(sistema_asovac = self.sistema_id, es_autor_principal = True, pagado = True, trabajo__estatus__iexact="aceptado")
        trabajos = []
        for autor_trabajo in autores_trabajos:
            trabajos.append((autor_trabajo.trabajo.id, autor_trabajo.trabajo.titulo_espanol))
        self.fields['trabajos'] = forms.MultipleChoiceField(  choices = trabajos,
                                                required=True,
                                                label="",
                                                widget=FilteredSelectMultiple("Trabajos", is_stacked=False))


class MultipleRecipientsWithDateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(MultipleRecipientsWithDateForm, self).__init__(*args, **kwargs)
        # create a new recipients_name blank field
        field1_name = 'recipients_name_0'
        self.fields[field1_name] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={'placeholder':'Nombre Completo',
                                          'class':'form-control new-list-item'})
        )
        # create a new recipients_email blank field
        field2_name = 'recipients_email_0'
        self.fields[field2_name] = forms.EmailField(
            required=False,
            widget=forms.EmailInput(attrs={'placeholder':'Correo Electrónico',
                                            'class':'form-control new-list-item'})
        )

        # create a new recipients_event_name blank field
        field3_name = 'recipients_event_name'
        self.fields[field3_name] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder':'Nombre del evento',
                                          'class':'form-control'})
        )
        self.fields[field3_name].label = "Nombre del evento"

        # create a new recipients_date blank field
        field4_name = 'recipients_date'
        self.fields[field4_name] = forms.DateField(
            widget=forms.TextInput(attrs={'placeholder':'Fecha: dd/mm/AAAA',
                                          'class':'form-control dateinput'})
        )
        self.fields[field4_name].label = "Fecha de evento"

    def get_name_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_name_'):
                yield self[field_name]

    def get_email_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_email_'):
                yield self[field_name]


class MultipleRecipientsWithDateAndSubjectForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(MultipleRecipientsWithDateAndSubjectForm, self).__init__(*args, **kwargs)
        # create a new recipients_name blank field
        field1_name = 'recipients_name_0'
        self.fields[field1_name] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={'placeholder':'Nombre Completo',
                                          'class':'form-control new-list-item'})
        )
        # create a new recipients_email blank field
        field2_name = 'recipients_email_0'
        self.fields[field2_name] = forms.EmailField(
            required=False,
            widget=forms.EmailInput(attrs={'placeholder':'Correo Electrónico',
                                            'class':'form-control new-list-item'})
        )

        # create a new recipients_event_name blank field
        field3_name = 'recipients_event_name'
        self.fields[field3_name] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder':'Nombre del evento',
                                          'class':'form-control'})
        )
        self.fields[field3_name].label = "Nombre del evento"

        # create a new recipients_date blank field
        field4_name = 'recipients_date'
        self.fields[field4_name] = forms.DateField(
            widget=forms.TextInput(attrs={'placeholder':'Fecha: dd/mm/AAAA',
                                          'class':'form-control dateinput'})
        )
        self.fields[field4_name].label = "Fecha de evento"

        # create a new recipients_event_name blank field
        field3_name = 'recipients_conference_name'
        self.fields[field3_name] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder':'Título de la conferencia',
                                          'class':'form-control'})
        )
        self.fields[field3_name].label = "Nombre de la conferencia"

    def get_name_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_name_'):
                yield self[field_name]

    def get_email_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_email_'):
                yield self[field_name]


class MultipleRecipientsWithRoleForm(forms.Form):
    ROLE_OPTIONS = (
        ('asistente', 'Asistente'),
        ('autor', 'Autor'),
        ('conferencista', 'Conferencista'),
    )

    role = forms.ChoiceField(
        label="Tipo de Portanombre",
        required=True,
        choices=ROLE_OPTIONS,
        widget=forms.Select(attrs={'class':'form-control'})
    )


    def __init__(self, *args, **kwargs):
        super(MultipleRecipientsWithRoleForm, self).__init__(*args, **kwargs)
        # create a new recipients_name blank field
        field1_name = 'recipients_name_0'
        self.fields[field1_name] = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={'placeholder':'Nombre Completo',
                                          'class':'form-control new-list-item'})
        )
        # create a new recipients_email blank field
        field2_name = 'recipients_email_0'
        self.fields[field2_name] = forms.EmailField(
            required=False,
            widget=forms.EmailInput(attrs={'placeholder':'Correo Electrónico',
                                           'class':'form-control new-list-item'})
        )

        # create a new recipients_event_name blank field
        
class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=100)
    file = forms.FileField(label="Archivo",widget=forms.FileInput(attrs={'accept': 'image/png, image/jpeg, image/gif'}))

     
class resumenContentForm(forms.Form):
    # title = forms.CharField(max_length=100)
    content = forms.CharField(label="Contenido para el PDF",widget=forms.Textarea(attrs={'cols': 80, 'rows': 20, 'id':"content"}))

class resumenPalabrasForm(forms.Form):
    presidenteNombre = forms.CharField(label="Introduzca su nombre",max_length=200)
    presidenteCargo = forms.CharField(label="Introduzca su cargo",max_length=200)
    presidenteContenido = forms.CharField(label="Introduzca unas breves palabras",widget=forms.Textarea(attrs={'cols': 80, 'rows': 20, 'id':"presidenteContenido"}))
    cabecera = forms.CharField(label="Introduzca el texto de la cabecera",required=False,widget=forms.Textarea(attrs={'cols': 80, 'rows': 10, 'id':"cabecera"}))
    secretarioNombre = forms.CharField(label="Introduzca su nombre",max_length=200,required=False)
    secretarioCargo = forms.CharField(label="Introduzca su cargo",required=False,max_length=200)
    secretarioContenido = forms.CharField(label="Introduzca unas breves palabras",required=False,widget=forms.Textarea(attrs={'cols': 80, 'rows': 20, 'id':"secretarioContenido"}))

class UploadAficheForm(forms.Form):
    # title = forms.CharField(max_length=100)
    afiche_titulo = forms.CharField(label="Introduzca el título para el afiche",required=True,max_length=200)
    file = forms.FileField(label="Archivo",widget=forms.FileInput(attrs={'accept': 'image/png, image/jpeg, image/gif'}))


class comisionAcademicaForm(forms.Form):
    coordinadores_area = forms.CharField(label="Introduzca el nombre de los coordinadores de área",widget=forms.Textarea(attrs={'cols': 80, 'rows': 10, 'id':"coordinadoresArea"}))
    titulo_comision = forms.CharField(label="Introduzca el título para los miembros de la comisión",required=True,max_length=200)
    miembros_comision = forms.CharField(label="Introduzca el nombre de los miembros de la comisión",widget=forms.Textarea(attrs={'cols': 80, 'rows': 15, 'id':"miembrosComision"}))
    