# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from django.core.urlresolvers import reverse

from .models import Sistema_asovac, Usuario_asovac, Rol, Area, Sub_area
from django.forms import CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


estados_arbitraje = (   (0,'Desactivado'),
                        (1,'Iniciado'),
                        (2,'En Selección y Asignación de Coordinadores de Área'),
                        (3,'En Carga de Trabajos'),
                        (4,'En Asignación de Trabajos a las Áreas'),
                        (5,'En En Arbitraje'),
                        (6,'En Cierre de Arbitraje'),
                        (7,'En Asignación de Secciones'),
                        (8,'En Resumen'))

class RegisterForm(UserCreationForm):

    class Meta:
        model= User
        fields = ['username','first_name','last_name','email',]


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
    name_arbitration = forms.CharField(label="Nombre arbitraje", max_length=20)
    description = forms.CharField(label="Descripción", max_length=255)
    start_date = forms.DateField(label="Fecha de inicio")
    end_date = forms.DateField(label="Fecha de fin")
        
        # super(MyLoginForm, self).__init__(*args, **kwargs)
        # self.helper = FormHelper()
        # self.helper.form_id = 'login-form'
        # self.helper.form_method = 'post'
        # #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
        # self.helper.add_input(Submit('submit', 'Ingresar', css_class='btn-block'))

class CreateArbitrajeForm(forms.ModelForm):

    class Meta:
        model = Sistema_asovac
        fields = ['nombre','descripcion', 'fecha_inicio_arbitraje', 'fecha_fin_arbitraje']

    def __init__(self, *args, **kwargs):
        super(CreateArbitrajeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'create-arbitraje-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-8'
        #self.helper.form_action = reverse('/') # <-- CHANGE THIS LINE TO THE NAME OF LOGIN VIEW
        #self.helper.add_input(Submit('submit', 'Crear', css_class='btn-success btn-lg pull-right'))
        self.helper.layout = Layout( # the order of the items in this layout is important
            'nombre',
            Field('descripcion', rows="4"),
            'fecha_inicio_arbitraje',
            'fecha_fin_arbitraje',
            Div(
                Div(
                    HTML("<a href=\"{% url 'main_app:home' %}\" class=\"btn btn-danger btn-block btn-lg\">Cancelar</a>"),
                css_class='col-sm-2 col-sm-offset-7'),

                Div(
                    Submit('submit', 'Crear', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
                css_class='col-sm-2'),

                Div(
                    HTML("<a href=\"#\" class=\"btn btn-info btn-lg btn-block\" data-toggle=\"modal\" data-target=\"#modal-success\">Ver</a>"),
                css_class='col-sm-1'),

            css_class='row')
        )

class PerfilForm(forms.ModelForm):
    
    class Meta:
        model= User
        fields=['username','first_name','last_name','email',]

class AdminAssingRolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminAssingRolForm, self).__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.filter(id__gt=1)
        self.fields['rol'].required = True

    class Meta:
        model = Usuario_asovac
        fields = ['rol']
        widgets = {'rol': CheckboxSelectMultiple()}

class CoordGeneralAssingRolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CoordGeneralAssingRolForm, self).__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.filter(id__gt=2)
        self.fields['rol'].required = True

    class Meta:
        model = Usuario_asovac
        fields = ['rol']
        widgets = {'rol': CheckboxSelectMultiple()}

class CoordAreaAssingRolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CoordAreaAssingRolForm, self).__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.filter(id__gt=3)
        self.fields['rol'].required = True

    class Meta:
        model = Usuario_asovac
        fields = ['rol']
        widgets = {'rol': CheckboxSelectMultiple()}

class ArbitrajeAssignCoordGenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArbitrajeAssignCoordGenForm, self).__init__(*args, **kwargs)
                                                        # El rol con id 2 es Coordinador General
        self.fields['coordinador_general'].queryset = Usuario_asovac.objects.filter(rol__id = 2)
        self.fields['coordinador_general'].required = True

    class Meta:
        model = Sistema_asovac
        fields = ['coordinador_general']


class ArbitrajeStateChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArbitrajeStateChangeForm, self).__init__(*args, **kwargs)
        self.fields['estado_arbitraje'].required = True

    class Meta:
        model = Sistema_asovac
        fields = ['coordinador_general', 'estado_arbitraje']
        widgets = {'coordinador_general': forms.HiddenInput(),
                'estado_arbitraje': forms.Select(choices = estados_arbitraje, attrs={'class': "form-control"})}

    def clean_coordinador_general(self):
        data = self.cleaned_data['coordinador_general']
        if data is None:
            print ('Raising form error of estado!')
            raise forms.ValidationError("¡Este arbitraje no posee Coordinador General! Asigne uno para continuar.")
        return data


class RolForm(forms.ModelForm):
    class Meta:
        model= Usuario_asovac
        fields=['rol']

class AreaForm(forms.ModelForm):
    class Meta:
        model= Area
        fields=['nombre']

class SubareaForm(forms.ModelForm):
    class Meta:
        model= Sub_area
        fields=['nombre']
