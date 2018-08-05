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

## Esta es la función encargada de generar una respuesta PDF para una carta de aceptacion de resumen CON observaciones.
def generate_acceptation_letter_with_observations(filename, context):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=' + filename

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, firstLineIndent=48))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Work_Title', alignment=TA_CENTER, leftIndent=24, rightIndent=24))
    styles.add(ParagraphStyle(name='IdentedBullets',  alignment=TA_JUSTIFY, bulletFontSize = 14, bulletIndent = 96, leftIndent=110, rightIndent=24))

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

    ptext = '<font size=10>Para tener una versión de su trabajo acorde a lo solicitado en la normativa del\
    evento, leagradecesmos incorporar las siguiente correciones indicadas por los árbitros:</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ## Añadimos las observaciones pertinentes, estas vienen en una List de strings.
    ptext = '<font size=10><b>Observaciones</b></font>' 
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    for observation in context["observations"]:
        ptext = '<bullet>&bull;</bullet>%s' % observation
        Story.append(Paragraph(ptext, styles["IdentedBullets"]))
        Story.append(Spacer(1, 3))
    Story.append(Spacer(1, 21))

    ptext = '<font size=10>Le agradecemos suministrar la nueva versión del resumen a más tardar en <b>tres (3) días</b>, a \
    partir de la fecha de envío de esta comunicación, mediante el <font color=blue><u><link href="%s">Formulario de registro \
    de la versión final del resumen (haga click para abrir el formulario)</link></u></font>.</font>' % context["completed_work_form_link"]
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

## Esta es la función encargada de generar una respuesta PDF para una carta de rechazo de resumen CON observaciones.
def generate_rejection_letter_with_observations(filename, context):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=' + filename

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)
    Story=[]

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, firstLineIndent=48))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Work_Title', alignment=TA_CENTER, leftIndent=24, rightIndent=24))
    styles.add(ParagraphStyle(name='IdentedBullets',  alignment=TA_JUSTIFY, bulletFontSize = 14, bulletIndent = 96, leftIndent=110, rightIndent=24))

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

    # Añadimos el resto del texto de rechazo
    areas_string = ""
    if len(context["deficient_areas"]) > 1:
        areas_string = ", ".join(context["deficient_areas"][:-1]) + " y " + context["deficient_areas"][-1]
    else:
        areas_string = context["deficient_areas"][0]

    ptext = '<font size=10>Identificado con el código <b>%s</b> ha sido debidamente arbitrado. Los \
    miembros del Jurado evaluador han manifestado que el resumen del trabajo presenta deficiencias en algunos \
    siguientes aspectos: %s.</font>' % (context["work_code"], areas_string)
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ptext = '<font size=10>Razón por la cuel el <b>resumen No fue aceptado</b> para su presentación en la \
    %s Convención Anual de AsoVAC. A continuación se indican las observaciones de los árbitros:</font>' % context["roman_number"]
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ## Añadimos las observaciones pertinentes, estas vienen en una List de strings.
    ptext = '<font size=10><b>Observaciones</b></font>' 
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 6))
    for observation in context["observations"]:
        ptext = '<bullet>&bull;</bullet>%s' % observation
        Story.append(Paragraph(ptext, styles["IdentedBullets"]))
        Story.append(Spacer(1, 3))
    Story.append(Spacer(1, 21))

    ptext = '<font size=10>Invitamos cordialmente a los autores a complementar el trabajo realizando, mejorando y \
    ampliando su resumen, a  fin de presentarlo a evaluación en otro evento o en la próxima Convención Anual AsoVAC, \
    divulgando así el trabajo realizado y su aporte en la comunidad.</font>'
    Story.append(Paragraph(ptext, styles["Justify"]))
    Story.append(Spacer(1, 12))

    ptext = '<font size=10>Quedando a sus órdenes, se despide.</font>'
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
    context["observations"] =   ['El resumen no cumple con el formato indicado en la normativa de la Convención y el modelo enviado.',
                                'No se cumple con lo solicitado para el formato de nombres y apellidos de los autores completos, separados por coma.',
                                'La ventaja evidente del consumo de edulcorantes no calóricos es reducir el aporte calórico proveniente de sacarosa y \
                                otros endulzantes que sí aportan carbohidratos, pero ningún edulcorante conocido tiene poder hipoglicemiante. Tampoco tiene \
                                poder adelgazante per sé. Todo depende del resto del aporte de macronutrientes y otras condiciones de gasto calórico V/S requerimiento.',
                                'No están claros los porcentajes de ingesta definidos para los tres grupos.',
                                'Falta señalar cuantitativamente la reducción ponderal y en cuánto tiempo además de expresarlo con significancia y análisis estadístico.',
                                'Es conocido el after taste de la Stevia, sería interesante informar si los animales mostraron alguna preferencia o rechazo por las tres opciones propuestas.']
    context["deficient_areas"] = ['metodología', 'resultados', 'conclusiones', 'palabras clave']
    context["completed_work_form_link"] = 'https://docs.google.com/forms/d/e/1FAIpQLSdJsmghAty674AII18VKDbQDOv3-1b4jhZtJfqBouzYFwJL3g/viewform'

    return generate_acceptation_letter_with_observations(filename, context)
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

