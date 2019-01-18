# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _ #usado para personalizar las etiquetas de los formularios
from .models import Sistema_asovac, Usuario_asovac, Rol, Area, Sub_area,Usuario_rol_in_sistema
from .validators import valid_extension

estados_arbitraje = (   (0,'Desactivado'),
                        (1,'Iniciado'),
                        (2,'En Selección y Asignación de Coordinadores de Área'),
                        (3,'En Carga de Trabajos'),
                        (4,'En Asignación de Trabajos a las Áreas'),
                        (5,'En En Arbitraje'),
                        (6,'En Cierre de Arbitraje'),
                        (7,'En Asignación de Secciones'),
                        (8,'En Resumen'))

my_date_formats = ['%d/%m/%Y']
my_date_format = '%d/%m/%Y'

#Formulario para cambiar la contraseña.
class ChangePassForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePassForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = "Contraseña actual"
        self.fields['new_password1'].label = "Nueva contraseña"
        self.fields['new_password2'].label = "Confirmar contraseña"

    #Este codigo no lanza el mensaje
    def clean_old_password(self):
        password = self.cleaned_data['old_password']
        if not self.user.check_password(password):
            print ("La Contraseña es invalida: Old Password")
            raise forms.ValidationError(_("La contraseña es incorrecta."),code='invalid_password')
        return password

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        if password1.isdigit():
            raise forms.ValidationError(_("La contraseña no puede ser completamente númerica"), code="new_password_numeric")
        return password1

    #Este codigo no lanza el mensaje.
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 != password2:
            raise forms.ValidationError(_("Las nuevas contraseñas no coinciden."), code = "new_password")
        return password2


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
    start_date = forms.DateField(label="Fecha de inicio", input_formats=my_date_formats)
    end_date = forms.DateField(label="Fecha de fin", input_formats=my_date_formats)

class CreateArbitrajeForm(forms.ModelForm):

    class Meta:
        model = Sistema_asovac
        fields = ['nombre','descripcion', 'fecha_inicio_arbitraje', 'fecha_fin_arbitraje','porcentaje_iva', 'monto_pagar_trabajo']
        widgets = {'fecha_inicio_arbitraje': forms.DateInput(format=my_date_format),
                   'fecha_fin_arbitraje': forms.DateInput(format=my_date_format)}
        labels = {'descripcion': 'Descripción', 'fecha_fin_arbitraje': 'Fecha de Culminación', 'fecha_inicio_arbitraje': 'Fecha de Inicio','porcentaje_iva' : 'Porcentaje del IVA', 'monto_pagar_trabajo' : 'Monto para postular trabajos'}

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
            'porcentaje_iva', 
            'monto_pagar_trabajo',
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

class AssingRolForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.max_role = kwargs.pop('max_role')
    #     self.user_asovac = kwargs.pop('user_asovac')
    #     super(AssingRolForm, self).__init__(*args, **kwargs)
       
        # print "test: ", Usuario_rol_in_sistema.objects.filter(rol_id__gt=self.max_role, usuario_asovac_id=self.user_asovac).query
        # # self.fields['rol'].queryset = Usuario_rol_in_sistema.objects.filter(rol_id__gt=self.max_role, usuario_asovac_id=self.user_asovac)
        # self.fields['rol'].queryset = Usuario_rol_in_sistema.objects.filter(rol_id__gt=self.max_role, usuario_asovac_id=self.user_asovac)
        # self.fields['rol'].required = True
    class Meta:
        model = Usuario_rol_in_sistema
        fields = ['rol','usuario_asovac','sistema_asovac']
        # widgets = {'rol': CheckboxSelectMultiple()}


class ArbitrajeAssignCoordGenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArbitrajeAssignCoordGenForm, self).__init__(*args, **kwargs)
                                                        # El rol con id 2 es Coordinador General
        self.fields['coordinador_general'].queryset = Usuario_asovac.objects.all()
        self.fields['coordinador_general'].required = True

    class Meta:
        model = Sistema_asovac
        fields = ['coordinador_general']
        widgets = {'coordinador_general': forms.Select(attrs={'class': 'form-control'})}


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

"""
class RolForm(forms.ModelForm):
    class Meta:
        model= Usuario_asovac
        fields=['rol']
"""
class AreaForm(forms.ModelForm):
    class Meta:
        model= Area
        fields=['nombre']

class AreaCreateForm(forms.ModelForm):
    class Meta:
        model= Area
        fields=['nombre','descripcion']

class SubareaForm(forms.ModelForm):
    class Meta:
        model= Sub_area
        fields=['nombre']

class SubAreaRegistForm(forms.ModelForm):
    class Meta:
        model= Usuario_asovac
        fields=['sub_area',]
        labels={'sub_area':'Subrea',}
        widget={
            'sub_area': forms.CheckboxSelectMultiple(),
        }

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=100)
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': '.xls, .csv, .xlsx'}))
