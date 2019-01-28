from __future__ import unicode_literals

from django import forms
from .models import Arbitro

class ArbitroForm(forms.ModelForm):
    class Meta:
        model= Arbitro
        fields=['nombres','apellidos','genero','cedula_pasaporte','correo_electronico','titulo','linea_investigacion','telefono_oficina','telefono_habitacion_celular','institucion_trabajo','datos_institucion','observaciones']
