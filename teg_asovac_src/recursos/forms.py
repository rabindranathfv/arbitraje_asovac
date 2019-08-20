# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML, Row, Column

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from main_app.models import Usuario_rol_in_sistema
from arbitrajes.models import Arbitro


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
        self.fields[field1_name] = forms.CharField(required=False)
        # create a new recipients_email blank field
        field2_name = 'recipients_email_0'
        self.fields[field2_name] = forms.EmailField(required=False)

    def clean(self):
        cleaned_data = super(MultipleRecipientsForm, self).clean()
        recipients_names = list()
        recipients_emails = list()
        i = 0
        field1_name = 'recipients_name_%s' % (i)
        field2_name = 'recipients_email_%s' % (i)
        while self.cleaned_data.get(field1_name):
            recipients_name = cleaned_data.get(field1_name)
            recipients_email = cleaned_data.get(field2_name)
            # Si existe un destinatario sin su email asociado
            # Se levanta un error de validacion:
            if recipients_name and not recipients_email:
                raise forms.ValidationError(
                    "Todos los destinatarios deben poseer un email asociado."
                )
            else:
                recipients_names.append(recipients_name)
                recipients_emails.append(recipients_email)
            i += 1
            field1_name = 'recipients_name_%s' % (i)
            field2_name = 'recipients_email_%s' % (i)
        self.cleaned_data["recipients_names"] = recipients_names
        self.cleaned_data["recipients_emails"] = recipients_emails

    def get_name_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_name_'):
                yield self[field_name]

    def get_email_fields(self):
        for field_name in self.fields:
            if field_name.startswith('recipients_email_'):
                yield self[field_name]
