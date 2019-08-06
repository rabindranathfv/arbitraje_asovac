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
    img_w, img_h = img.getSize()
    aspect = img_h / float(img_w)
    return Image(path, width=width, height=(width * aspect))


# Esta clase permite generar cartas dado un contexto.
class LetterGenerator:

    def __init__(self):
        self.styles = None
        self.context = None

    def _set_buffer_and_styles(self):
        my_buffer = BytesIO()

        doc = SimpleDocTemplate(
            my_buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=24,
            bottomMargin=48
        )

        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, firstLineIndent=48))
        self.styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        self.styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(name='Work_Title', alignment=TA_CENTER, leftIndent=24,
                                       rightIndent=24))
        self.styles.add(ParagraphStyle(name='IdentedBullets', alignment=TA_JUSTIFY, bulletFontSize=14,
                                       bulletIndent=48, leftIndent=60, rightIndent=24))

        return my_buffer, doc

    def _add_header_date_and_greetings(self, story):
        ## Insertando el Header como imagen a partir de una URL si esta es válida
        try:
            im = get_image(self.context["header_url"], width=6.5*inch)
            im.hAlign = 'CENTER'
            story.append(im)
            story.append(Spacer(1, 36))
        except:
            pass

        ## Aquí añadimos la fecha a la derecha del documento.
        ptext = '<font size=10>%s, %s de %s de %s</font>' % (self.context["city"], self.context["day"],
                                                             self.context["month"], self.context["year"])
        story.append(Paragraph(ptext, self.styles["Right"]))
        story.append(Spacer(1, 12))

        # Añadimos el saludo a la izquierda dependiendo del genero del autor a quien va dirigido.
        if self.context["sex"] == 'F':
            ptext = '<font size=10><b>Estimada Investigadora:<br/>%s,</b></font>' % self.context["full_name"].strip()
        else:
            ptext = '<font size=10><b>Estimado Investigador:<br/>%s,</b></font>' % self.context["full_name"].strip()
        story.append(Paragraph(ptext, self.styles["Normal"]))
        story.append(Spacer(1, 24))

    def _add_paper_details_and_authors(self, story):
        # Añadir el primer parrafo:
        ptext = '<font size=10>Reciba un cordial saludo del Comité Organizador de la %s Convención Anual de AsoVAC,\
         en ocasión de informarle que el resumen titulado:</font>' % self.context["roman_number"]
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        # Añadir el título del resumen aceptado:
        ptext = '<font size=11><b>%s</b></font>' % self.context["work_title"]
        story.append(Paragraph(ptext, self.styles["Work_Title"]))
        story.append(Spacer(1, 12))

        # Añadir los autores del resumen aceptado
        if len(self.context["authors"]) > 1:
            ptext = '<font size=10>Autores:</font>'
        else:
            ptext = '<font size=10>Autor:</font>'
        story.append(Paragraph(ptext, self.styles["Normal"]))
        story.append(Spacer(1, 8))

        ptext = '<font size=11><b>%s</b></font>' % ", ".join(self.context["authors"])
        story.append(Paragraph(ptext, self.styles["Work_Title"]))
        story.append(Spacer(1, 12))

    def _add_final_greeting(self, story):
        ptext = '<font size=10>Saludos cordiales,</font>'
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 36))

        ptext = '<font size=10>Comité Organizador<br/> %s Convención Anual AsoVAC</font>' % self.context["roman_number"]
        story.append(Paragraph(ptext, self.styles["Center"]))
        story.append(Spacer(1, 12))


    ## Esta es la función encargada de generar una respuesta PDF para una
    ## carta de aceptacion de resumen
    def get_approval_letter(self, filename, context):
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
        self.context = context
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + filename

        my_buffer, doc = self._set_buffer_and_styles()

        story = []

        self._add_header_date_and_greetings(story)

        self._add_paper_details_and_authors(story)

        # Añadimos el resto del texto de aceptacion
        ptext = '<font size=10>Identificado con el código <b>%s</b> ha sido debidamente arbitrado y\
         <b>aceptado para su presentación</b> en la Convención Anual que se realizará desde el %s hasta el %s, \
        en espacios de la %s y bajo el lema <b>%s</b>.</font>' % (self.context["work_code"],
                                                                  self.context["start_date"],
                                                                  self.context["finish_date"],
                                                                  self.context["convention_place"],
                                                                  self.context["convention_saying"])
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        ptext = '<font size=10>A más tardar el %s le informaremos el lugar, hora y sesión de\
         presentación de su trabajo.</font>' % self.context["max_info_date"]
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        ptext = '<font size=10>Agradecemos su participación y aprovechamos para invitarlo a asistir\
         a los distintos eventos a realizarse en el marco de la Convención.</font>'
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 36))

        self._add_final_greeting(story)

        doc.build(story)

        pdf = my_buffer.getvalue()
        my_buffer.close()
        response.write(pdf)

        return response

    ## Esta es la función encargada de generar una respuesta PDF para una
    ## carta de aceptacion de resumen CON observaciones.
    def get_approval_letter_w_obs(self, filename, context):
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
        self.context = context
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + filename

        my_buffer, doc = self._set_buffer_and_styles()

        story = []

        self._add_header_date_and_greetings(story)

        self._add_paper_details_and_authors(story)

        # Añadimos el resto del texto de aceptacion
        ptext = '<font size=10>Identificado con el código <b>%s</b> ha sido debidamente arbitrado y \
        <b>aceptado para su presentación</b> en la Convención Anual que se realizará desde el %s hasta el %s, \
        en espacios de la %s y bajo el lema <b>%s</b>.</font>' % (self.context["work_code"],
                                                                  self.context["start_date"],
                                                                  self.context["finish_date"],
                                                                  self.context["convention_place"],
                                                                  self.context["convention_saying"])
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        ptext = '<font size=10>Para tener una versión de su trabajo acorde a lo solicitado en la\
         normativa del evento, leagradecesmos incorporar las siguiente correciones indicadas por\
         los árbitros:</font>'
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        ## Añadimos las observaciones pertinentes, estas vienen en una List de strings.
        ptext = '<font size=10><b>Observaciones</b></font>'
        story.append(Paragraph(ptext, self.styles["Normal"]))
        story.append(Spacer(1, 6))
        for observation in self.context["observations"]:
            ptext = '<bullet>&bull;</bullet>%s' % observation
            story.append(Paragraph(ptext, self.styles["IdentedBullets"]))
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 21))

        ptext = '<font size=10>Le agradecemos suministrar la nueva versión del resumen a más tardar\
         en <b>tres (3) días</b>, a partir de la fecha de envío de esta comunicación, mediante el\
         <font color=blue><u><link href="%s">Formulario de registro de la versión final del resumen\
         (haga click para abrir el formulario)</link></u></font>.</font>' % self.context["completed_work_form_link"]
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        ptext = '<font size=10>A más tardar el %s le informaremos el lugar, hora y sesión de\
         presentación de su trabajo.</font>' % self.context["max_info_date"]
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        ptext = '<font size=10>Agradecemos su participación y aprovechamos para invitarlo a asistir\
         a los distintos eventos a realizarse en el marco de la Convención.</font>'
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 36))

        self._add_final_greeting(story)

        doc.build(story)

        pdf = my_buffer.getvalue()
        my_buffer.close()
        response.write(pdf)

        return response

    ## Esta es la función encargada de generar una respuesta PDF para una carta de rechazo de resumen CON observaciones.
    def get_rejection_letter_w_obs(self, filename, context):
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
        self.context = context
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + filename

        my_buffer, doc = self._set_buffer_and_styles()

        story = []

        self._add_header_date_and_greetings(story)

        self._add_paper_details_and_authors(story)

        # Añadimos el resto del texto de rechazo
        areas_string = ""
        if len(self.context["deficient_areas"]) > 1:
            areas_string = ", ".join(self.context["deficient_areas"][:-1])
            areas_string += " y " + self.context["deficient_areas"][-1]
        else:
            areas_string = self.context["deficient_areas"][0]

        ptext = '<font size=10>Identificado con el código <b>%s</b> ha sido debidamente arbitrado.\
         Los miembros del Jurado evaluador han manifestado que el resumen del trabajo presenta\
         deficiencias en algunos siguientes aspectos: %s.</font>' % (self.context["work_code"],
                                                                     areas_string)
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        ptext = '<font size=10>Razón por la cuel el resumen <b>No fue aceptado</b> para su\
         presentación en la %s Convención Anual de AsoVAC. A continuación se indican las\
         observaciones de los árbitros:</font>' % self.context["roman_number"]
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        ## Añadimos las observaciones pertinentes, estas vienen en una List de strings.
        ptext = '<font size=10><b>Observaciones</b></font>'
        story.append(Paragraph(ptext, self.styles["Normal"]))
        story.append(Spacer(1, 6))
        for observation in self.context["observations"]:
            ptext = '<bullet>&bull;</bullet>%s' % observation
            story.append(Paragraph(ptext, self.styles["IdentedBullets"]))
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 21))

        ptext = '<font size=10>Invitamos cordialmente a los autores a complementar el trabajo\
         realizando, mejorando y ampliando su resumen, a  fin de presentarlo a evaluación en otro\
         evento o en la próxima Convención Anual AsoVAC, divulgando así el trabajo realizado y\
         su aporte en la comunidad.</font>'
        story.append(Paragraph(ptext, self.styles["Justify"]))
        story.append(Spacer(1, 12))

        self._add_final_greeting(story)

        doc.build(story)

        pdf = my_buffer.getvalue()
        my_buffer.close()
        response.write(pdf)

        return response


# Esta clase permite generar certificados dado un contexto.
class CertificateGenerator:

    def __init__(self):
        self.styles = None
        self.context = None

    def _set_buffer_and_styles(self):
        my_buffer = BytesIO()

        doc = SimpleDocTemplate(
            my_buffer,
            pagesize=landscape(letter),
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )

        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Simple', alignment=TA_LEFT, leftIndent=48))
        self.styles.add(ParagraphStyle(name='DocType', alignment=TA_LEFT, leftIndent=48,
                                       fontName='Times-Roman'))
        self.styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, firstLineIndent=48))
        self.styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        self.styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(name='Authors', alignment=TA_CENTER, leftIndent=24,
                                       rightIndent=24, fontSize=22, leading=28, textColor=ReportLabBlue))
        self.styles.add(ParagraphStyle(name='Work_Title', alignment=TA_CENTER, leftIndent=60,
                                       rightIndent=60, fontSize=20, leading=24,))
        self.styles.add(ParagraphStyle(name='IdentedBullets', alignment=TA_JUSTIFY,
                                       bulletFontSize=14, bulletIndent=48, leftIndent=60, rightIndent=24))

        return my_buffer, doc

    ## Esta es la función encargada de generar una respuesta PDF para un certificado de autores.
    def get_authors_certificate(self, context, filename):
        """
        Esta función requiere las siguientes variables por contexto para hacer render pdf correctamente:
        - context["header_url"]
        - context["city"] = String con el nombre de la Ciudad donde se desarrolla la Asovac.
        - context["authority1_info"] = Informacion formateada de la autoridad1
        - context["signature1_path"] = Camino local de la imagen de la firma1
        - context["authority2_info"] = Informacion formateada de la autoridad2
        - context["signature2_path"] = Camino local de la imagen de la firma2
        - context["logo_path"] = Camino local de la imagen del logo
        - context['date_string'] = String con la Fecha en formato 'DD de Mes de AAAA'
        - context["work_title"] = String que representa el nombre del trabajo completo.
        - context["authors"] = Lista de Strings con nombres  de los autores del paper.

        """
        self.context = context
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + filename

        my_buffer, doc = self._set_buffer_and_styles()

        story = []

        try:
            header_img = get_image(self.context["header_url"], width=10*inch)
            header_img.hAlign = 'CENTER'
            story.append(header_img)
            story.append(Spacer(1, 24))
        except:
            pass

        ## Primera línea del certificado.
        ptext = '<font size=15>La Asociación Venezolana para el Avance de la Ciencia (AsoVAC)\
         otorga el presente</font>'
        story.append(Paragraph(ptext, self.styles["Simple"]))
        story.append(Spacer(1, 12))

        ## Tipo de Documento
        ptext = '<font size=36><b>CERTIFICADO</b> a:</font>'
        story.append(Paragraph(ptext, self.styles["DocType"]))
        story.append(Spacer(1, 40))

        ## Autores del paper.
        ptext = '<font><b>%s</b></font>' % ", ".join(self.context["authors"])
        story.append(Paragraph(ptext, self.styles["Authors"]))
        story.append(Spacer(1, 16))

        ## Presentando y colocando el titulo del paper
        ptext = '<font size=15>Por la presentación de la ponencia del trabajo libre:</font>'
        story.append(Paragraph(ptext, self.styles["Simple"]))
        story.append(Spacer(1, 12))

        ptext = '<font><b>%s</b></font>' % self.context["work_title"]
        story.append(Paragraph(ptext, self.styles["Work_Title"]))
        story.append(Spacer(1, 12))

        doc.build(story, onFirstPage=self.canvas_footer_editing)

        pdf = my_buffer.getvalue()
        my_buffer.close()
        response.write(pdf)

        return response

    def canvas_footer_editing(self, canvas, doc):
        # En esta funcion, se dibuja el borde y los elementos del
        # footer del certificado utilizando el canvas del documento.
        footer_height = 55
        page_width, page_height = landscape(letter)
        signature_width = 2*inch
        logo_width = 1.2*inch

        canvas.saveState()
        #Agregar borde del certificado
        canvas.rect(30, 30, 732, 552, stroke=1, fill=0)
        # Primera autoridad y su firma
        signature1 = get_image(self.context["signature1_path"], width=signature_width)
        # Se ubica a un quinto del documento a partir del margen
        x_coord = (page_width / 5) + 50 - (signature_width / 2)
        y_coord = footer_height + 20
        signature1.drawOn(canvas, x_coord, y_coord)

        paragraph = Paragraph("""<font size=12>%s</font>""" % self.context["authority1_info"],
                              self.styles['Right'])
        paragraph.wrapOn(canvas, 200, 50)
        paragraph.drawOn(canvas, 90, footer_height)

        # Segunda autoridad y su firma
        signature2 = get_image(self.context["signature2_path"], width=signature_width)
        # Se ubica a tres cuartos del documento a partir del margen
        x_coord = (3 * page_width / 4) + 30 - (signature_width / 2)
        signature2.drawOn(canvas, x_coord, y_coord)
        paragraph = Paragraph("""<font size=12>%s</font>""" % self.context["authority2_info"],
                              self.styles['Normal'])
        paragraph.wrapOn(canvas, 200, 50)
        paragraph.drawOn(canvas, 510, footer_height)

        # Fecha y Sello de AsoVAC
        asovac_logo = get_image(self.context["logo_path"], width=logo_width)
        asovac_logo.drawOn(canvas, 350, footer_height)
        paragraph = Paragraph("""<font size=10>%s %s</font>""" % (self.context["city"],
                                                                  self.context["date_string"]),
                              self.styles['Center'])
        paragraph.wrapOn(canvas, 200, 50)
        paragraph.drawOn(canvas, 295, footer_height-18)

        canvas.restoreState()
