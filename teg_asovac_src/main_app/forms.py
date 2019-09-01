# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML, Row, Column

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm,PasswordResetForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _ #usado para personalizar las etiquetas de los formularios
from .models import Sistema_asovac, Usuario_asovac, Rol, Area, Sub_area,Usuario_rol_in_sistema
from .validators import valid_extension
from django.core.exceptions import ValidationError

from arbitrajes.models import Arbitro

estados_arbitraje = (   (0,'Desactivado'),
                        (1,'Iniciado'),
                        (2,'En Selección y Asignación de Coordinadores de Área'),
                        (3,'En Carga de Trabajos'),
                        (4,'En Asignación de Trabajos a las Áreas'),
                        (5,'En Arbitraje'),
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


class DataBasicForm(forms.ModelForm):
    class Meta:
        model = Sistema_asovac
        fields = (
            'nombre',
            'descripcion',
            'fecha_inicio_arbitraje',
            'fecha_fin_arbitraje',
            'cabecera',
            'color_fondo_pie',
            'color_letras_pie',
            'autoridad1',
            'firma1',
            'autoridad2',
            'firma2',
            'logo',
            'ciudad',
            'numero_romano'
        )
        widgets = {
            'fecha_inicio_arbitraje': forms.DateInput(format=my_date_format),
            'fecha_fin_arbitraje': forms.DateInput(format=my_date_format)
        }
        labels = {
            'descripcion': 'Descripción',
            'fecha_fin_arbitraje': 'Fecha de Culminación',
            'fecha_inicio_arbitraje': 'Fecha de Inicio',
            'cabecera': 'URL de Imagen Cabecera',
            'color_fondo_pie': 'Color de Pie de Página',
            'color_letras_pie': 'Color Texto de Pie de Página',
            'ciudad': 'Ciudad',
            'numero_romano': 'Número Romano',
        }
        help_texts = {
            'autoridad1': 'Para desplegar texto en una nueva línea, inserte una coma Ej. "Linea1,Linea2"',
            'autoridad2': 'Para desplegar texto en una nueva línea, inserte una coma Ej. "Linea1,Linea2"',
            'numero_romano': 'Número de la convención en números romanos para desplegar en cartas y certificados',
        }

    def __init__(self, *args, **kwargs):
        super(DataBasicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'edit-arbitraje-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = Layout( # the order of the items in this layout is important
            'nombre',
            Field('descripcion', rows="4"),
            'fecha_inicio_arbitraje',
            'fecha_fin_arbitraje',
            HTML("""<h3 style="margin-left:30px; margin-top:40px">Personalización de Correos</h3><hr>""", ),
            'cabecera',
            Div(
                HTML("""{% if form.cabecera.value %}<label class="control-label col-sm-3">Imagen de Cabecera Actual</label>{% endif %}""", ),
                Div(
                    HTML("""{% if form.cabecera.value %}<img src="{{ form.cabecera.value }}" alt="Preview Cabecera ASOVAC" style="width:100%; border: 1px solid #999;">{% endif %}""", ),
                    css_class='controls col-sm-8'
                ),
                css_class='form-group'
            ),
            'color_fondo_pie',
            'color_letras_pie',
            Div(
                HTML(
                    """
                    {% if form.color_letras_pie.value and form.color_fondo_pie.value %}
                    <div class="col-sm-offset-3 col-sm-8" style="border-radius: 5px; margin-bottom: 18px; border: 1px solid #999; height: 50px; background-color: {{ form.color_fondo_pie.value }};">
                        <p style="color: {{ form.color_letras_pie.value }}; font-size: 16px; padding-top: 12px;">
                            <b>Previsualización de Colores</b>
                        </p>
                    </div>
                    {% endif %}
                    """
                ,),
                css_class="row",
                style="padding-left: 15px;"
            ),
            HTML("""<h3 style="margin-left:30px; margin-top:40px">Personalización de Certificados</h3><hr>""", ),
            'ciudad',
            'numero_romano',
            'autoridad1',
            'firma1',
            Div(
                HTML("""{% if form.instance.firma1 %}<label class="control-label col-sm-3">Imagen de Firma Autoridad 1</label>{% endif %}""", ),
                Div(
                    HTML("""{% if form.instance.firma1 %}<img src="{{ form.instance.firma1.url }}" alt="Preview Firma 1" style="width:40%; border: 1px solid #999;">{% endif %}""", ),
                    css_class='controls col-sm-8'
                ),
                css_class='form-group'
            ),
            'autoridad2',
            'firma2',
            Div(
                HTML("""{% if form.instance.firma2 %}<label class="control-label col-sm-3">Imagen de Firma Autoridad 2</label>{% endif %}""", ),
                Div(
                    HTML("""{% if form.instance.firma2 %}<img src="{{ form.instance.firma2.url }}" alt="Preview Firma 1" style="width:40%; border: 1px solid #999;">{% endif %}""", ),
                    css_class='controls col-sm-8'
                ),
                css_class='form-group'
            ),
            'logo',
            Div(
                HTML("""{% if form.instance.logo.url %}<label class="control-label col-sm-3">Imagen de Logo</label>{% endif %}""", ),
                Div(
                    HTML("""{% if form.instance.logo.url %}<img src="{{ form.instance.logo.url }}" alt="Preview Firma 1" style="width:40%; border: 1px solid #999;">{% endif %}""", ),
                    css_class='controls col-sm-8'
                ),
                css_class='form-group'
            ),
            Div(
                Div(
                    Submit('submit', 'Guardar', css_class='btn-primary btn-block', css_id='btn-modal-success'),
                    css_class='col-sm-offset-9 col-sm-2'
                ),
                css_class='row',
                style="margin-bottom: 20px;"
            )
        )

    def clean(self):
        cleaned_data = super(DataBasicForm, self).clean()
        start_date = cleaned_data.get("fecha_inicio_arbitraje")
        end_date = cleaned_data.get("fecha_fin_arbitraje")

        if end_date <= start_date:
            # Si la fecha de culminación es igual o posterior a la fecha de inicio levantar un error.
            raise forms.ValidationError(
                "La fecha de culminación debe ser diferente y posterior a la fecha de inicio."
            )



class CreateArbitrajeForm(forms.ModelForm):

    class Meta:
        model = Sistema_asovac
        fields = [
            'nombre',
            'descripcion',
            'fecha_inicio_arbitraje',
            'fecha_fin_arbitraje',
            'porcentaje_iva',
            'monto_pagar_trabajo'
        ]
        widgets = {
            'fecha_inicio_arbitraje': forms.DateInput(format=my_date_format),
            'fecha_fin_arbitraje': forms.DateInput(format=my_date_format)
        }
        labels = {
            'descripcion': 'Descripción',
            'fecha_fin_arbitraje': 'Fecha de Culminación',
            'fecha_inicio_arbitraje': 'Fecha de Inicio',
            'porcentaje_iva' : 'Porcentaje del IVA',
            'monto_pagar_trabajo' : 'Monto para postular trabajos'
        }

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
                    css_class='col-sm-2 col-sm-offset-7'
                ),
                Div(
                    Submit('submit', 'Crear', css_class='btn-success btn-lg btn-block', css_id='btn-modal-success'),
                    css_class='col-sm-2'
                ),
                css_class='row'
            )
        )

    def clean(self):
        cleaned_data = super(CreateArbitrajeForm, self).clean()
        start_date = cleaned_data.get("fecha_inicio_arbitraje")
        end_date = cleaned_data.get("fecha_fin_arbitraje")

        if end_date <= start_date:
            # Si la fecha de culminación es igual o posterior a la fecha de inicio levantar un error.
            raise forms.ValidationError(
                "La fecha de culminación debe ser diferente y posterior a la fecha de inicio."
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


class ArbitrajeAssignCoordGenForm(forms.Form):
    # user_search=Usuario_rol_in_sistema.objects.filter(sistema_asovac = arbitraje_id).values_list('usuario_asovac_id', flat=True)
    # usuarios_test = Usuario_asovac.objects.exclude(id__in=user_search )
    # coordinador_general = forms.ModelChoiceField(queryset = Usuario_asovac.objects.exclude(id__in=user_search ).order_by('usuario__first_name'), label = '')
    # coordinador_general = forms.ModelChoiceField(queryset = Usuario_asovac.objects.all().order_by('usuario__first_name'), label = '')
    def __init__(self, *args, **kwargs):
        self.sistema_id = kwargs.pop('sistema_id')
        super(ArbitrajeAssignCoordGenForm, self).__init__(*args, **kwargs)
        user_search=Usuario_rol_in_sistema.objects.filter(sistema_asovac = self.sistema_id )
        # user_search=Usuario_rol_in_sistema.objects.filter(sistema_asovac = self.sistema_id ).values_list('usuario_asovac_id', flat=True)
        # usuarios_test = Usuario_asovac.objects.exclude(id__in=user_search )
        # list_users= Usuario_asovac.objects.exclude(id__in=user_search ).order_by('usuario__first_name')
        self.fields['coordinador_general'] = forms.ModelChoiceField(  
                                                queryset = Usuario_rol_in_sistema.objects.all().filter(sistema_asovac = self.sistema_id ).order_by('id'),
                                                required=True,
                                                label="",
                                                widget=forms.Select(attrs={'class':'form-control'}))
        # self.fields['coordinador_general'].widget.attrs['class'] = 'form-control'

class ArbitrajeStateChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArbitrajeStateChangeForm, self).__init__(*args, **kwargs)
        self.fields['estado_arbitraje'].required = True
        self.fields['estado_arbitraje'].label=''

    class Meta:
        model = Sistema_asovac
        fields = ['estado_arbitraje']
        widgets = {'estado_arbitraje': forms.Select(choices = estados_arbitraje, attrs={'class': "form-control"})}



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
        fields=['nombre','codigo','descripcion']
        labels={'nombre':'Nombre','codigo':'Código','descripcion':'Descripción'}

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
    file = forms.FileField(label="Archivo",widget=forms.FileInput(attrs={'accept': '.xls, .csv, .xlsx'}))

class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("El correo "+email+" no se encuentra registrado.")
        return email
    

class EditPersonalDataForm(forms.ModelForm):
    
    class Meta:
        model = Arbitro
        fields = ['nombres', 'apellidos', 'genero', 'cedula_pasaporte', 'correo_electronico']
        widgets = {
            'nombres': forms.TextInput(attrs={'placeholder': 'Ejemplo:Juan Enrique', }),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Ejemplo:Castro Rodriguez'}),
            'cedula_pasaporte': forms.TextInput(attrs={'placeholder': 'Formato: V para CI y P para pasaporte, seguido del número.'}),
            'correo_electronico': forms.TextInput(attrs={'placeholder': 'Ejemplo: juancastro@gmail.com'}),
        }

    confirm_email = forms.EmailField(label = "Confirmar correo electrónico",required=False)

    def __init__(self, *args, **kwargs):
        super(EditPersonalDataForm, self).__init__(*args, **kwargs)
        self.fields['confirm_email'].widget.attrs['placeholder'] = 'Repita el correo en caso de cambio'
        self.fields['genero'].label = 'Género'
        self.fields['cedula_pasaporte'].label = 'Cédula/Pasaporte'
        self.fields['correo_electronico'].label = 'Correo Electrónico'

    def clean_cedula_pasaporte(self):
        cedula_pasaporte = self.cleaned_data['cedula_pasaporte']
        pattern = re.compile('^(V|P)[0-9]+$')
        if not pattern.match(cedula_pasaporte):
            raise forms.ValidationError("Formato de cédula/pasaporte incorrecto, introduzca V o P seguido del número. Ejemplo: V500")
        return cedula_pasaporte
        
    def clean_nombres(self):
        nombres = self.cleaned_data['nombres']
        pattern = re.compile('^([a-zA-Z]+\s?){1,3}$')
        if not pattern.match(nombres):
            raise forms.ValidationError("El campo nombres no puede tener carácteres especiales, debe tener sus nombres separados de un solo espacio.")
        return nombres

    def clean_apellidos(self):
        nombres = self.cleaned_data['apellidos']
        pattern = re.compile('^([a-zA-Z]+\s?){1,3}$')
        if not pattern.match(nombres):
            raise forms.ValidationError("El campo apellidos no puede tener carácteres especiales, debe tener sus apellidos separados de un solo espacio.")
        return nombres

    def clean_confirm_email(self):
        correo_electronico_antiguo = self.instance.correo_electronico
        correo_electronico = self.cleaned_data['correo_electronico']
        correo_electronico_confirmacion = self.cleaned_data['confirm_email']
        if correo_electronico_antiguo != correo_electronico:
            if correo_electronico_confirmacion == "":
                raise forms.ValidationError("Se detectó un cambio en el correo elecrónico, por favor confirme el correo electrónico que desea cambiar.")
            elif correo_electronico_confirmacion != correo_electronico:
                raise forms.ValidationError("Confirmación del correo electrónico no coincide con el correo que desea asignar a su cuenta.")
        return correo_electronico_confirmacion

