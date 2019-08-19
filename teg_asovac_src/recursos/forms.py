# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Div, HTML, Row, Column

from django import forms

from django.contrib.admin.widgets import FilteredSelectMultiple
from main_app.models import Usuario_asovac
class CertificateToRefereeForm(forms.Form):
    arbitros = forms.ModelMultipleChoiceField(queryset=Usuario_asovac.objects.all(),
                                                required=True,
                                                widget=FilteredSelectMultiple("arbitros", is_stacked=False))
    def __init__(self, *args, **kwargs):
        super(CertificateToRefereeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div('arbitros', ),
            Submit('submit', 'Save Genes',
                   css_class="save btn btn-success")
        )
        

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',
               '/static/css/adminoverrides.css', ), } # custom css

        js = ('admin/js/vendor/jquery/jquery.js', 'admin/js/jquery.init.js','/static/jsi18n.js' )