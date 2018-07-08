# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.urlresolvers import reverse

class MyLoginForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=100)
    password = forms.CharField(label="Contraseña", max_length=100, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
       super(MyLoginForm, self).__init__(*args, **kwargs)
       self.helper = FormHelper()
       self.helper.form_id = 'login-form'
       self.helper.form_method = 'post'
       #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
       self.helper.add_input(Submit('submit', 'Ingresar', css_class='btn-block'))

class DataBasicForm(forms.Form):
    name_arbitration= forms.CharField(label="Nombre arbitraje", max_length=20)
    description= forms.CharField(label="Descripción", max_length=255)
    start_date= forms.DateField(label="Fecha de inicio")
    end_date= forms.DateField(label="Fecha de fin")