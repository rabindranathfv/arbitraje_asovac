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
# import para renderear un pdf a partir de una plantilla html
from io import BytesIO
from reportlab.pdfgen import canvas
import time
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Create your views here.
def recursos_pag(request):
    context = {
        "nombre_vista": 'recursos'
    }
    return render(request,"test_views.html",context)

## Esta es la función encargada de generar una respuesta PDF para una carta de aceptacion de resumen.
def generate_acceptation_letter(filename, context):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=' + filename

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
     
    formatted_time = time.ctime()
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, firstLineIndent=48))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Work_Title', alignment=TA_CENTER, leftIndent=24, rightIndent=24))

    ## Aquí añadimos la fecha a la derecha del documento.
    ptext = '<font size=10>%s, %s de %s de %s</font>' % (context["city"], context["day"], context["month"], context["year"])
    Story.append(Paragraph(ptext, styles["Right"]))
    Story.append(Spacer(1, 12))
     
    # Añadimos el saludo a la izquierda dependiendo del genero del autor a quien va dirigido.
    if context["sex"] == 'F':
        ptext = '<font size=10><b>Estimada Investigadora:<br/>%s,</b></font>' % context["full_name"].strip()
    else:
        ptext = '<font size=10><b>Estimado Investigador:<br/>%s,</b></font>' % context["full_name"].strip()
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 24))

    # Añadimos  el primer parrafo:
    ptext = '<font size=10>Reciba un cordial saludo del Comité Organizador de la %s Convención Anual de AsoVAC,\
     en ocasión de informarle que el resumen titulado:</font>' % context["roman_number"]
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    # Añadimos  el título del resumen aceptado:
    ptext = '<font size=11><b>%s</b></font>' % context["work_title"]
    Story.append(Paragraph(ptext, styles["Work_Title"]))
    Story.append(Spacer(1, 12))

    # Añadimos los autores del resumen aceptado
    if len(context["authors"]) > 1:
        ptext = '<font size=10>Autores:</font>'
    else:
        ptext = '<font size=10>Autor:</font>'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 8))

    ptext = '<font size=11><b>%s</b></font>' % ", ".join(context["authors"])
    Story.append(Paragraph(ptext, styles["Work_Title"]))
    Story.append(Spacer(1, 12))

    # Añadimos el resto del texto de aceptacion
    ptext = '<font size=10>Identificado con el código <b>%s</b> ha sido debidamente arbitrado y \
    <b>aceptado para su presentación</b> en la Convención Anual que se realizará desde el %s hasta el %s, \
    en espacios de la %s y bajo el lema <b>%s</b>.</font>' % (context["work_code"], context["start_date"], context["finish_date"], context["convention_place"], context["convention_saying"])
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ptext = '<font size=10>A más tardar el %s le informaremos el lugar, hora y sesión de presentación\
     de su trabajo.</font>' % context["max_info_date"]
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ptext = '<font size=10>Agradecemos su participación y aprovechamos para invitarlo a asistir a los distintos eventos a realizarse\
    en el marco de la Convención.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 36))

    ptext = '<font size=10>Saludos cordiales,</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 36))

    ptext = '<font size=10>Comité Organizador<br/> %s Convención Anual AsoVAC</font>' % context["roman_number"]
    Story.append(Paragraph(ptext, styles["Center"]))
    Story.append(Spacer(1, 12))

    doc.build(Story)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def generate_pdf(request,*args , **kwargs):
    filename = "AsoVAC_Carta_Aceptacion.pdf"
    context = {}
    context["city"] = 'Caracas'
    context["day"] = 4
    context["month"] = 'Agosto'
    context["year"] = 2018
    context["sex"] = 'F'
    context["full_name"] = 'Karla Calo'
    context["roman_number"] = 'LXVII'
    context["work_title"] = 'ESCALAMIENTO A ESCALA INDUSTRIAL DE UNA CREMA AZUFRADA OPTIMIZADA MEDIANTE\
    UN DISEÑO EXPERIMENTAL'
    context["work_code"] = 'BC-24'
    context["start_date"] = '29 de Noviembre'
    context["finish_date"] = '1 de Diciembre de 2018'
    context["convention_place"] = "Universidad Metropolintana (UNIMET) y la Universidad Central de Venezuela (UCV)"
    context["convention_saying"] = '"Ciencia, Tecnología e Innovación en Democracia"'
    context["authors"] = ['Karla Calo', 'Luis Henríquez']
    context["max_info_date"] = '15 de Noviembre'

    return generate_acceptation_letter(filename, context)
    """
    #obtener el template
    template = get_template('pdf/certificate_pdf_base.html')
    # hacer querysets
    
    # Data a renderizar en el template
    context = {}
    # render template
    html = template.render(context)
    # to download in pdf
    pdf = render_to_pdf('pdf/certificate_pdf_base.html',context)
    #respuesta del pdf en el navegador
    if pdf:
        return HttpResponse(pdf, content_type='application/pdf')
    return HttpResponse("Crear pagina de Error 404")
    """

def resources_author(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
    else:
        estado=0

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_author.html', context)

def resources_referee(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
    else:
        estado=0

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_referee.html', context)

def resources_event(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
    else:
        estado=0

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_event.html', context)

def resources_sesion(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
    else:
        estado=0

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_sesion.html', context)

def resources_asovac(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
    else:
        estado=0

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_asovac.html', context)

def resources_arbitration(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
    else:
        estado=0

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_arbitrations.html', context)

