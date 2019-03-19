from __future__ import unicode_literals
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML
from django import forms
from .models import Arbitro
from trabajos.models import Trabajo_arbitro
class ArbitroForm(forms.ModelForm):
    class Meta:
        model= Arbitro
        fields=['nombres','apellidos','genero','cedula_pasaporte','correo_electronico','titulo','linea_investigacion','telefono_oficina','telefono_habitacion_celular','institucion_trabajo','datos_institucion','observaciones']

class RefereeCommentForm(forms.ModelForm):

	class Meta:
		model = Trabajo_arbitro
		fields = ['comentario_autor']

	def __init__(self, *args, **kwargs):
		super(RefereeCommentForm,self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'referee-comment-form'
		self.helper.form_method = 'post'
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-sm-3'
		self.helper.field_class = 'col-sm-8'
		self.fields['comentario_autor'].required = True
		self.fields['comentario_autor'].label = "Comentario al autor"
		self.fields['comentario_autor'].widget.attrs['rows'] = 4