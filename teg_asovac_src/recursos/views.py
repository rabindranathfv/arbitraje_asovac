# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from django.http import HttpResponse

# import funcion in utils.py
from .utils import render_to_pdf
# for load template to render to pdf
from django.template.loader import get_template

# Create your views here.
def recursos_pag(request):
    context = {
        "nombre_vista": 'recursos'
    }
    return render(request,"test_views.html",context)

def generate_pdf(request,*args , **kwargs):
    #obtener el template
    template = get_template('pdf/modelo_pdf.html')
    # hacer querysets
    
    # Data a renderizar en el template
    context = {}
    # render template
    html = template.render(context)
    # to download in pdf
    pdf = render_to_pdf('pdf/modelo_pdf.html',context)
    #respuesta del pdf en el navegador
    if pdf:
        return HttpResponse(pdf, content_type='application/pdf')
    return HttpResponse("Crear pagina de Error 404")