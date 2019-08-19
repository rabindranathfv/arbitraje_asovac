# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML, Row, Column

from django import forms

from django.contrib.admin.widgets import FilteredSelectMultiple
from main_app.models import Usuario_asovac, Usuario_rol_in_sistema, Sistema_asovac
from arbitrajes.models import Arbitro
class CertificateToRefereeForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.sistema_id = kwargs.pop('sistema_id')
        super(CertificateToRefereeForm, self).__init__(*args, **kwargs)
        usuarios_arbitros_in_sistema = Usuario_rol_in_sistema.objects.filter(rol = 4, sistema_asovac = self.sistema_id, status = True)
        arbitros = []
        for usuario_arbitro_in_sistema in usuarios_arbitros_in_sistema:
            arbitro = Arbitro.objects.get(usuario = usuario_arbitro_in_sistema.usuario_asovac)
            arbitros.append((arbitro.id, arbitro.nombres))
        self.fields['arbitros'] = forms.MultipleChoiceField(  choices = arbitros,
                                                required=True,
                                                label="",
                                                widget=FilteredSelectMultiple("Arbitros", is_stacked=False))

    