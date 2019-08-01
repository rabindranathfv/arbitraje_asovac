# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from io import BytesIO
from reportlab.lib import utils
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.colors import ReportLabBlue
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

from django.conf import settings
from django.http import HttpResponse



def get_image(path, width=1*inch):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    print (iw, ih)
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def set_letter_pdf_buffer_and_styles():
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=24,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, firstLineIndent=48))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Work_Title', alignment=TA_CENTER, leftIndent=24, rightIndent=24))
    styles.add(ParagraphStyle(name='IdentedBullets', alignment=TA_JUSTIFY, bulletFontSize=14,
                              bulletIndent=48, leftIndent=60, rightIndent=24))

    return buffer, doc, styles


def set_certificate_pdf_buffer_and_styles():
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Simple', alignment=TA_LEFT, leftIndent=48))
    styles.add(ParagraphStyle(name='DocType', alignment=TA_LEFT, leftIndent=48, fontName='Times-Roman'))
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, firstLineIndent=48))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Authors', alignment=TA_CENTER, leftIndent=24, rightIndent=24,
                              fontSize=22, leading=28, textColor=ReportLabBlue))
    styles.add(ParagraphStyle(name='Work_Title', alignment=TA_CENTER, leftIndent=60, rightIndent=60,
                              fontSize=20, leading=24,))
    styles.add(ParagraphStyle(name='IdentedBullets', alignment=TA_JUSTIFY, bulletFontSize=14,
                              bulletIndent=48, leftIndent=60, rightIndent=24))

    return buffer, doc, styles


def append_pdf_header_date_and_greetings(story, context, styles):
    ## Insertando el Header como imagen a partir de una URL si esta es válida
    try:
        im = Image(context["header_url"])#, 0.1*inch, 0.1*inch
        im.hAlign = 'CENTER'
        im._restrictSize(6.5 * inch, 2 * inch)
        story.append(im)
        story.append(Spacer(1, 36))
    except:
        pass

    ## Aquí añadimos la fecha a la derecha del documento.
    ptext = '<font size=10>%s, %s de %s de %s</font>' % (context["city"], context["day"],
                                                         context["month"], context["year"])
    story.append(Paragraph(ptext, styles["Right"]))
    story.append(Spacer(1, 12))

    # Añadimos el saludo a la izquierda dependiendo del genero del autor a quien va dirigido.
    if context["sex"] == 'F':
        ptext = '<font size=10><b>Estimada Investigadora:<br/>%s,</b></font>' % context["full_name"].strip()
    else:
        ptext = '<font size=10><b>Estimado Investigador:<br/>%s,</b></font>' % context["full_name"].strip()
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 24))


def append_pdf_paper_details_and_authors(story, context, styles):
    # Añadimos  el primer parrafo:
    ptext = '<font size=10>Reciba un cordial saludo del Comité Organizador de la %s Convención Anual de AsoVAC,\
     en ocasión de informarle que el resumen titulado:</font>' % context["roman_number"]
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    # Añadimos  el título del resumen aceptado:
    ptext = '<font size=11><b>%s</b></font>' % context["work_title"]
    story.append(Paragraph(ptext, styles["Work_Title"]))
    story.append(Spacer(1, 12))

    # Añadimos los autores del resumen aceptado
    if len(context["authors"]) > 1:
        ptext = '<font size=10>Autores:</font>'
    else:
        ptext = '<font size=10>Autor:</font>'
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 8))

    ptext = '<font size=11><b>%s</b></font>' % ", ".join(context["authors"])
    story.append(Paragraph(ptext, styles["Work_Title"]))
    story.append(Spacer(1, 12))


def append_pdf_final_greetings(story, context, styles):
    ptext = '<font size=10>Saludos cordiales,</font>'
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 36))

    ptext = '<font size=10>Comité Organizador<br/> %s Convención Anual AsoVAC</font>' % context["roman_number"]
    story.append(Paragraph(ptext, styles["Center"]))
    story.append(Spacer(1, 12))


## Esta es la función encargada de generar una respuesta PDF para una carta de aceptacion de resumen.
def generate_acceptation_letter(filename, context):
    """
    Esta función requiere las siguientes variables por contexto para hacer un render en pdf correcto:
    - context["header_url"]
    - context["city"] = String con el nombre de la Ciudad donde se desarrolla la Asovac.
    - context["day"] = Integer representando el día del mes de la fecha actual.
    - context["month"] = String del nombre del mes de la fecha actual.
    - context["year"] = Integer representando el año de la fecha actual.
    - context["sex"] = Un caracter 'M' o 'F' indicando el genero de a quien va dirigida la carta.
    - context["full_name"] = String con el nombre completo a quien va dirigida la carta.
    - context["roman_number"] = String representando el numero de la convención asovac.
    - context["work_title"] = String que representa el nombre del trabajo completo.
    - context["authors"] = Lista de Strings con nombres  de los autores del paper.
    - context["work_code"] = String que indica el codigo del trabajo.
    - context["start_date"] = String con la fecha de inicio de la convención asovac
    - context["finish_date"] = String con la fecha final de la convención asovac
    - context["convention_place"] = String con el nombre del lugar de la convención asovac
    - context["convention_saying"] = String con el slogan o dicho de la convención actual.
    - context["completed_work_form_link"] = String con la url del enlace de registro/actualización del trabajo
    - context["max_info_date"] = String con la fecha máximo de aviso al autor para la presentación de su trabajo.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=' + filename

    buffer, doc, styles = set_letter_pdf_buffer_and_styles()

    story = []

    append_pdf_header_date_and_greetings(story, context, styles)

    append_pdf_paper_details_and_authors(story, context, styles)

    # Añadimos el resto del texto de aceptacion
    ptext = '<font size=10>Identificado con el código <b>%s</b> ha sido debidamente arbitrado y \
    <b>aceptado para su presentación</b> en la Convención Anual que se realizará desde el %s hasta el %s, \
    en espacios de la %s y bajo el lema <b>%s</b>.</font>' % (context["work_code"],
                                                              context["start_date"], context["finish_date"],
                                                              context["convention_place"], context["convention_saying"])
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=10>A más tardar el %s le informaremos el lugar, hora y sesión de presentación\
     de su trabajo.</font>' % context["max_info_date"]
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=10>Agradecemos su participación y aprovechamos para invitarlo a asistir a los distintos eventos a realizarse\
    en el marco de la Convención.</font>'
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 36))

    append_pdf_final_greetings(story, context, styles)

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

## Esta es la función encargada de generar una respuesta PDF para una carta de aceptacion de resumen CON observaciones.
def generate_acceptation_letter_with_observations(filename, context):
    """
    Esta función requiere las siguientes variables por contexto para hacer un render en pdf correcto:
    - context["header_url"]
    - context["city"] = String con el nombre de la Ciudad donde se desarrolla la Asovac.
    - context["day"] = Integer representando el día del mes de la fecha actual.
    - context["month"] = String del nombre del mes de la fecha actual.
    - context["year"] = Integer representando el año de la fecha actual.
    - context["sex"] = Un caracter 'M' o 'F' indicando el genero de a quien va dirigida la carta.
    - context["full_name"] = String con el nombre completo a quien va dirigida la carta.
    - context["roman_number"] = String representando el numero de la convención asovac.
    - context["work_title"] = String que representa el nombre del trabajo completo.
    - context["authors"] = Lista de Strings con nombres  de los autores del paper.
    - context["work_code"] = String que indica el codigo del trabajo.
    - context["observations"] = Lista de Strings
    - context["start_date"] = String con la fecha de inicio de la convención asovac
    - context["finish_date"] = String con la fecha final de la convención asovac
    - context["convention_place"] = String con el nombre del lugar de la convención asovac
    - context["convention_saying"] = String con el slogan o dicho de la convención actual.
    - context["completed_work_form_link"] = String con la url del enlace de registro/actualización del trabajo
    - context["max_info_date"] = String con la fecha máximo de aviso al autor para la presentación de su trabajo.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=' + filename

    buffer, doc, styles = set_letter_pdf_buffer_and_styles()

    story = []

    append_pdf_header_date_and_greetings(story, context, styles)

    append_pdf_paper_details_and_authors(story, context, styles)

    # Añadimos el resto del texto de aceptacion
    ptext = '<font size=10>Identificado con el código <b>%s</b> ha sido debidamente arbitrado y \
    <b>aceptado para su presentación</b> en la Convención Anual que se realizará desde el %s hasta el %s, \
    en espacios de la %s y bajo el lema <b>%s</b>.</font>' % (context["work_code"], context["start_date"], context["finish_date"], context["convention_place"], context["convention_saying"])
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=10>Para tener una versión de su trabajo acorde a lo solicitado en la normativa del\
    evento, leagradecesmos incorporar las siguiente correciones indicadas por los árbitros:</font>'
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    ## Añadimos las observaciones pertinentes, estas vienen en una List de strings.
    ptext = '<font size=10><b>Observaciones</b></font>'
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 6))
    for observation in context["observations"]:
        ptext = '<bullet>&bull;</bullet>%s' % observation
        story.append(Paragraph(ptext, styles["IdentedBullets"]))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 21))

    ptext = '<font size=10>Le agradecemos suministrar la nueva versión del resumen a más tardar en <b>tres (3) días</b>, a \
    partir de la fecha de envío de esta comunicación, mediante el <font color=blue><u><link href="%s">Formulario de registro \
    de la versión final del resumen (haga click para abrir el formulario)</link></u></font>.</font>' % context["completed_work_form_link"]
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=10>A más tardar el %s le informaremos el lugar, hora y sesión de presentación\
     de su trabajo.</font>' % context["max_info_date"]
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=10>Agradecemos su participación y aprovechamos para invitarlo a asistir a los distintos eventos a realizarse\
    en el marco de la Convención.</font>'
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 36))

    append_pdf_final_greetings(story, context, styles)

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

## Esta es la función encargada de generar una respuesta PDF para una carta de rechazo de resumen CON observaciones.
def generate_rejection_letter_with_observations(filename, context):
    """
    Esta función requiere las siguientes variables por contexto para hacer un render en pdf correcto:
    - context["header_url"]
    - context["city"] = String con el nombre de la Ciudad donde se desarrolla la Asovac.
    - context["day"] = Integer representando el día del mes de la fecha actual.
    - context["month"] = String del nombre del mes de la fecha actual.
    - context["year"] = Integer representando el año de la fecha actual.
    - context["sex"] = Un caracter 'M' o 'F' indicando el genero de a quien va dirigida la carta.
    - context["full_name"] = String con el nombre completo a quien va dirigida la carta.
    - context["roman_number"] = String representando el numero de la convención asovac.
    - context["work_title"] = String que representa el nombre del trabajo completo.
    - context["authors"] = Lista de Strings con nombres  de los autores del paper.
    - context["deficient_areas"] = Lista de Strings con los nombres de las areas.
    - context["work_code"] = String que indica el codigo del trabajo.
    - context["observations"] = Lista de Strings
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=' + filename

    buffer, doc, styles = set_letter_pdf_buffer_and_styles()

    story = []

    append_pdf_header_date_and_greetings(story, context, styles)

    append_pdf_paper_details_and_authors(story, context, styles)

    # Añadimos el resto del texto de rechazo
    areas_string = ""
    if len(context["deficient_areas"]) > 1:
        areas_string = ", ".join(context["deficient_areas"][:-1]) + " y " + context["deficient_areas"][-1]
    else:
        areas_string = context["deficient_areas"][0]

    ptext = '<font size=10>Identificado con el código <b>%s</b> ha sido debidamente arbitrado. Los \
    miembros del Jurado evaluador han manifestado que el resumen del trabajo presenta deficiencias en algunos \
    siguientes aspectos: %s.</font>' % (context["work_code"], areas_string)
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    ptext = '<font size=10>Razón por la cuel el resumen <b>No fue aceptado</b> para su presentación en la \
    %s Convención Anual de AsoVAC. A continuación se indican las observaciones de los árbitros:</font>' % context["roman_number"]
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    ## Añadimos las observaciones pertinentes, estas vienen en una List de strings.
    ptext = '<font size=10><b>Observaciones</b></font>'
    story.append(Paragraph(ptext, styles["Normal"]))
    story.append(Spacer(1, 6))
    for observation in context["observations"]:
        ptext = '<bullet>&bull;</bullet>%s' % observation
        story.append(Paragraph(ptext, styles["IdentedBullets"]))
        story.append(Spacer(1, 3))
    story.append(Spacer(1, 21))

    ptext = '<font size=10>Invitamos cordialmente a los autores a complementar el trabajo realizando, mejorando y \
    ampliando su resumen, a  fin de presentarlo a evaluación en otro evento o en la próxima Convención Anual AsoVAC, \
    divulgando así el trabajo realizado y su aporte en la comunidad.</font>'
    story.append(Paragraph(ptext, styles["Justify"]))
    story.append(Spacer(1, 12))

    append_pdf_final_greetings(story, context, styles)

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

## Esta es la función encargada de generar una respuesta PDF para un certificado de autores.
def generate_authors_certificate(filename, context):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=' + filename

    buffer, doc, styles = set_certificate_pdf_buffer_and_styles()

    story = []

    #doc.showBoundary = 1

    try:
        im = get_image(context["header_url"], width=10*inch)
        #im = Image(context["header_url"], width=10*inch)#, 0.1*inch, 0.1*inch
        im.hAlign = 'CENTER'
        story.append(im)
        story.append(Spacer(1, 24))
    except:
        pass

    ## Primera línea del certificado.
    ptext = '<font size=15>La Asociación Venezolana para el Avance de la Ciencia (AsoVAC) otorga el presente</font>'
    story.append(Paragraph(ptext, styles["Simple"]))
    story.append(Spacer(1, 12))

    ## Tipo de Documento
    ptext = '<font size=36><b>CERTIFICADO</b> a:</font>'
    story.append(Paragraph(ptext, styles["DocType"]))
    story.append(Spacer(1, 40))

    ## Autores del paper.
    ptext = '<font><b>%s</b></font>' % ", ".join(context["authors"])
    story.append(Paragraph(ptext, styles["Authors"]))
    story.append(Spacer(1, 16))

    ## Presentando y colocando el titulo del paper
    ptext = '<font size=15>Por la presentación de la ponencia del trabajo libre:</font>'
    story.append(Paragraph(ptext, styles["Simple"]))
    story.append(Spacer(1, 12))

    ptext = '<font><b>%s</b></font>' % context["work_title"]
    story.append(Paragraph(ptext, styles["Work_Title"]))
    story.append(Spacer(1, 12))

    doc.build(story, onFirstPage=canvas_footer_editing)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def canvas_footer_editing(canvas, doc):

    logo_path = os.path.join(settings.STATIC_ROOT, "img", "AsoVac_Logo.jpg")
    signature_path = 'http://help.itc.ihu.edu.gr/pki/ds/dg_img/signature_sample.jpg'
    footer_height = 55
    page_width, page_height = landscape(letter)
    signature_width = 2*inch
    logo_width = 1.2*inch

    default_styles = getSampleStyleSheet()
    default_styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    default_styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))

    canvas.saveState()
    #Agregar borde del certificado
    canvas.rect(30, 30, 732, 552, stroke=1, fill=0)
    # Primera autoridad y su firma
    signature1 = get_image(signature_path, width=signature_width)
    # Se ubica a un cuarto del documento a partir del margen
    x_coord = (page_width / 5) + 30 - (signature_width / 2)
    y_coord = footer_height + 20
    signature1.drawOn(canvas, x_coord, y_coord)

    paragraph = Paragraph("""<font size=12>Dr. Rafael Arturo Vasquez Balza<br/>Secretario General<br/>AsoVAC Capítulo Caracas</font>""",
                          default_styles['Right'])
    paragraph.wrapOn(canvas, 200, 50)
    paragraph.drawOn(canvas, 90, footer_height)

    # Segunda autoridad y su firma
    signature2 = get_image(signature_path, width=signature_width)
    x_coord = (3 * page_width / 4) + 30 - (signature_width / 2)
    signature2.drawOn(canvas, x_coord, y_coord)
    paragraph = Paragraph("""<font size=12>Dra. Marisol Aguilera Meneses<br/>Presidente<br/>AsoVAC</font>""",
                          default_styles['Normal'])
    paragraph.wrapOn(canvas, 200, 50)
    paragraph.drawOn(canvas, 510, footer_height)

    # Fecha y Sello de AsoVAC
    asovac_logo = get_image(logo_path, width=logo_width)
    asovac_logo.drawOn(canvas, 350, footer_height)
    paragraph = Paragraph("""<font size=10>Caracas 30 de Diciembre de 2017</font>""",
                          default_styles['Center'])
    paragraph.wrapOn(canvas, 200, 50)
    paragraph.drawOn(canvas, 295, footer_height-18)

    canvas.restoreState()
