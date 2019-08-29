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

    # def clean(self):
    #     cleaned_data = super(MultipleRecipientsForm, self).clean()
    #     print cleaned_data
    #     recipients_names = list()
    #     recipients_emails = list()
    #     i = 0
    #     field1_name = 'recipients_name_%s' % (i)
    #     field2_name = 'recipients_email_%s' % (i)
    #     while self.cleaned_data.get(field1_name):
    #         recipients_name = cleaned_data.get(field1_name)
    #         recipients_email = cleaned_data.get(field2_name)
    #         # Si existe un destinatario sin su email asociado o viceversa
    #         # Se levanta un error de validacion:
    #         if not (recipients_name and recipients_email):
    #             raise forms.ValidationError(
    #                 "Todos los destinatarios deben poseer un nombre y correo electrónico asociados."
    #             )
    #         else:
    #             recipients_names.append(recipients_name)
    #             recipients_emails.append(recipients_email)
    #         i += 1
    #         field1_name = 'recipients_name_%s' % (i)
    #         field2_name = 'recipients_email_%s' % (i)
    #     self.cleaned_data["recipients_names"] = recipients_names
    #     self.cleaned_data["recipients_emails"] = recipients_emails

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
            widget=forms.TextInput(attrs={'placeholder':'Fecha',
                                          'class':'form-control dateinput'})
        )
        self.fields[field4_name].label = "Fecha de evento"

    # def clean(self):
    #     cleaned_data = super(MultipleRecipientsForm, self).clean()
    #     print cleaned_data
    #     recipients_names = list()
    #     recipients_emails = list()
    #     i = 0
    #     field1_name = 'recipients_name_%s' % (i)
    #     field2_name = 'recipients_email_%s' % (i)
    #     while self.cleaned_data.get(field1_name):
    #         recipients_name = cleaned_data.get(field1_name)
    #         recipients_email = cleaned_data.get(field2_name)
    #         # Si existe un destinatario sin su email asociado o viceversa
    #         # Se levanta un error de validacion:
    #         if not (recipients_name and recipients_email):
    #             raise forms.ValidationError(
    #                 "Todos los destinatarios deben poseer un nombre y correo electrónico asociados."
    #             )
    #         else:
    #             recipients_names.append(recipients_name)
    #             recipients_emails.append(recipients_email)
    #         i += 1
    #         field1_name = 'recipients_name_%s' % (i)
    #         field2_name = 'recipients_email_%s' % (i)
    #     self.cleaned_data["recipients_names"] = recipients_names
    #     self.cleaned_data["recipients_emails"] = recipients_emails

    def get_name_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_name_'):
                yield self[field_name]

    def get_email_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_email_'):
                yield self[field_name]
    
    def get_event_name_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_event_name_'):
                yield self[field_name]

    def get_date_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_date_'):
                yield self[field_name]


