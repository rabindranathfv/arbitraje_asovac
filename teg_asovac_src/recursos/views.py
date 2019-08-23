# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random

from decouple import config

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.utils.timezone import now as timezone_now

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from arbitrajes.models import Arbitro
from autores.models import Autores_trabajos, Autor

from main_app.models import Usuario_rol_in_sistema, Rol, Sistema_asovac, Usuario_asovac, Area
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status

from trabajos.models import Trabajo_arbitro

from .utils import CertificateGenerator, LetterGenerator#, generate_authors_certificate
from .forms import CertificateToRefereeForm, CertificateToAuthorsForm, MultipleRecipientsForm


MONTH_NAMES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
               'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

TOP_NAVBAR_OPTIONS = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

class ChartData(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        arbitraje_id = request.session['arbitraje_id']
        #El siguiente codigo es para obtener los datos necesarios para la grafica de resultados de trabajos
        trabajos_aceptados = Autores_trabajos.objects.filter(sistema_asovac = arbitraje_id, pagado = True, es_autor_principal = True, trabajo__estatus = "Aceptado").count()
        trabajos_rechazados = Autores_trabajos.objects.filter(sistema_asovac = arbitraje_id, pagado = True, es_autor_principal = True, trabajo__estatus = "Rechazado").count()
        trabajos_pendientes = Autores_trabajos.objects.filter(sistema_asovac = arbitraje_id, pagado = True, es_autor_principal = True, trabajo__estatus = "Pendiente").count()
        
        #El siguiente codigo es para obtener los datos necesarios para la grafica de datos de arbitrajes y datos de area
        total_arbitros = Usuario_rol_in_sistema.objects.filter(rol = 4, sistema_asovac = arbitraje_id, status = True).count()
        autores_trabajos = Autores_trabajos.objects.filter(sistema_asovac = arbitraje_id, pagado = True)
        invitaciones_aceptadas = 0
        invitaciones_pendientes = 0
        
        areas_info = []
        areas_list = Area.objects.all() 
        for item in areas_list:
            areas_info.append({
                "id": item.id,
                "nombre": item.nombre,
                "trabajos_aceptados": 0,
                "trabajos_rechazados": 0,
                "cantidad_autores":0,
                "autores_id": []
                })
        
        for autor_trabajo in autores_trabajos:
            if autor_trabajo.es_autor_principal:    
                invitaciones_aceptadas += Trabajo_arbitro.objects.filter(trabajo = autor_trabajo.trabajo, invitacion = True).count()
                invitaciones_pendientes += Trabajo_arbitro.objects.filter(trabajo = autor_trabajo.trabajo, invitacion = False, fin_arbitraje = False).count()
            for item in areas_info:
                if autor_trabajo.trabajo.subareas.first().area.id == item["id"]:
                    if not autor_trabajo.autor.id in item["autores_id"]:
                        item["autores_id"].append(autor_trabajo.autor.id)
                    
                    if autor_trabajo.trabajo.estatus == "Aceptado" and autor_trabajo.es_autor_principal:
                        item["trabajos_aceptados"] += 1
                    elif autor_trabajo.trabajo.estatus == "Rechazado" and autor_trabajo.es_autor_principal:
                        item["trabajos_rechazados"] += 1


        areas_labels = []
        areas_trabajos_aceptados = []
        areas_trabajos_rechazados = []
        areas_autores = []
        areas_colores = []
        areas_labels_splited = []
        for item in areas_info:
            areas_labels.append(item["nombre"])
            areas_labels_splited.append(abreviate_if_neccesary(item["nombre"]))
            areas_trabajos_aceptados.append(item["trabajos_aceptados"])
            areas_trabajos_rechazados.append(item["trabajos_rechazados"])
            areas_autores.append(len(item["autores_id"]))
            areas_colores.append(generate_random_color())

        #El siguiente codigo es para obtener los datos necesarios para la grafica de niveles de intruccion de los autores
        usuarios_autor = Usuario_rol_in_sistema.objects.filter(rol = 5, sistema_asovac = arbitraje_id, status = True)
        educacion_primaria = 0
        educacion_secundaria = 0
        bachillerato = 0
        tecnico = 0
        universidad = 0
        postgrado = 0
        for usuario_autor in usuarios_autor:
            try:
                autor = Autor.objects.get(usuario = usuario_autor.usuario_asovac)
                if autor.nivel_instruccion == "Educación Básica Primaria":
                    educacion_primaria += 1
                elif autor.nivel_instruccion == "Educación Básica Secundaria":
                    educacion_secundaria += 1
                elif autor.nivel_instruccion == "Bachillerato/Educación Media":
                    bachillerato += 1
                elif autor.nivel_instruccion == "Educación Técnico/Profesional":
                    tecnico += 1
                elif autor.nivel_instruccion == "Universidad":
                    universidad += 1
                else:
                    postgrado += 1
            except: 
                pass


        data = {
            "trabajos": {
                "labels": ["Trabajos Aceptados", "Trabajos Rechazados", "Trabajos Pendientes"],
                "data": [trabajos_aceptados, trabajos_rechazados, trabajos_pendientes]
            },
            "arbitros": {
                "labels": ['Total árbitros', 'Invitaciones aceptadas', 'Invitaciones pendientes'],
                "data": [total_arbitros, invitaciones_aceptadas, invitaciones_pendientes]
            },
            "autores": {
                "labels": ['Educación Básica Primaria', 'Educación Básica Secundaria', 'Bachillerato/Educación Media', 'Educación Técnico/Profesional', 'Universidad', 'Postgrado'],
                "data": [educacion_primaria, educacion_secundaria, bachillerato, tecnico, universidad, postgrado]
            },
            "area":{
                "labels": areas_labels_splited,
                "data_aceptados": areas_trabajos_aceptados,
                "data_rechazados": areas_trabajos_rechazados,
            },
            "autoresArea":{
                "labels": areas_labels,
                "data": areas_autores,
                "colores": areas_colores
            },
        }   
        return Response(data)


# Funcion de ayuda que genera un contexto comun para todas las vistas/views
def create_common_context(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id = get_roles(request.user.id, arbitraje_id)
    item_active = 1
    items = validate_rol_status(estado, rol_id, item_active, arbitraje_id)
    route_conf = get_route_configuracion(estado, rol_id, arbitraje_id)
    route_seg = get_route_seguimiento(estado, rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado, rol_id, item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado, rol_id)
    route_resultados = get_route_resultados(estado, rol_id, arbitraje_id)

    context = {
        'main_navbar_options' : TOP_NAVBAR_OPTIONS,
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }

    return context


def generate_random_color():
    letras = "0123456789ABCDEF"
    color = "#"
    for x in range(0,6):
        color += letras[random.randint(0,15)]
    return color


def create_certificate_context(arbitraje):
    now = timezone_now()
    now_date_string = '%s de %s de %s' % (now.day, MONTH_NAMES[now.month - 1], now.year)
    path1 = arbitraje.firma1.url.replace('/media/', '')
    path2 = arbitraje.firma2.url.replace('/media/', '')
    path_logo = arbitraje.logo.url.replace('/media/', '')

    context = {}
    context["city"] = arbitraje.ciudad
    context["header_url"] = arbitraje.cabecera
    context["authority1_info"] = arbitraje.autoridad1.replace(',', '<br/>')
    context["signature1_path"] = os.path.join(os.path.join(settings.MEDIA_ROOT), path1)
    context["authority2_info"] = arbitraje.autoridad2.replace(',', '<br/>')
    context["signature2_path"] = os.path.join(os.path.join(settings.MEDIA_ROOT), path2)
    context["logo_path"] = os.path.join(os.path.join(settings.MEDIA_ROOT), path_logo)
    context['date_string'] = now_date_string
    context["roman_number"] = arbitraje.numero_romano

    # context["recipient_name"] = 'Rabindranath Ferreira'
    # context['event_name_string'] = 'LXVII Convencion Anual AsoVAC'
    # context['event_date_string'] = now_date_string
    # context['date_string'] = now_date_string
    # context["subject_title"] = 'EVALUACIÓN DE LA OBTENCIÓN DE ACEITE ESENCIAL DE SARRAPIA (DIPTERYX\
    #  ODORATA) EMPLEANDO CO2 COMO FLUIDO SUPERCRÍTICO Y MACERACIÓN ASISTIDA CON ULTRASONIDO'
    # context["people_names"] = ['Rabindranath Ferreira'] * 5
    # context["peoples_id"] = 'V-6.186.871'

    return context


def abreviate_if_neccesary(area_nombre):
    nombre_abreviado = ""
    if len(area_nombre) > 20:
        for item in area_nombre.split(" "):
            if item[0].isupper():
                nombre_abreviado += item[0]
        return nombre_abreviado
    return area_nombre


# Create your views here.
@login_required
def recursos_pag(request):
    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    return render(request, 'recursos.html', context)

def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)


@login_required
def generate_pdf(request,*args , **kwargs):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)

    filename = "AsoVAC_Certificado_Autores.pdf"

    context = {}
    context["header_url"] = arbitraje.cabecera
    context["city"] = 'Caracas'
    context["day"] = 4
    context["month"] = 'Agosto'
    context["year"] = 2018
    context["sex"] = 'F'
    context["full_name"] = 'Karla Calo'
    context["roman_number"] = 'LXVII'
    context["work_title"] = 'EVALUACIÓN DE LA OBTENCIÓN DE ACEITE ESENCIAL DE SARRAPIA (DIPTERYX ODORATA)\
     EMPLEANDO CO2 COMO FLUIDO SUPERCRÍTICO Y MACERACIÓN ASISTIDA CON ULTRASONIDO'
    context["work_code"] = 'BC-24'
    context["start_date"] = '29 de Noviembre'
    context["finish_date"] = '1 de Diciembre de 2018'
    context["convention_place"] = "Universidad Metropolintana (UNIMET) y la Universidad Central de Venezuela (UCV)"
    context["convention_saying"] = '"Ciencia, Tecnología e Innovación en Democracia"'
    context["authors"] = ['Rabindranath Ferreira'] * 5
    #['Karla Calo', 'Luis Henríquez', 'Laura Margarita Febres', 'Yoleida Soto Anes','Karla Calo', 'Luis Henríquez', 'Laura Margarita Febres']
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
    context["footer_content"] = """http://www.asovac.org/lxvii-convencion-anual-de-asovac https://www.facebook.com/ConvencionAsovac2017<br/>(0212)753-5802 asovac.convencion2017@gmail.com"""
    letters_gen = LetterGenerator()

    return letters_gen.get_rejection_letter_w_obs(filename, context)


@login_required
def create_approval_letters(request):
    pass


@login_required
def create_authors_certificates(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)

    context = create_certificate_context(arbitraje)

    certificate_gen = CertificateGenerator()

    return certificate_gen.get_authors_certificate(context)


@login_required
def resources_author(request):

    # print (rol_id)
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
    # print items
    if request.method == "POST":
        form = CertificateToAuthorsForm(request.POST, sistema_id = arbitraje_id)
        if form.is_valid():
            cert_context = create_certificate_context(arbitraje)
            for trabajo_id in form.cleaned_data['trabajos']:
                autores_trabajo = Autores_trabajos.objects.filter(trabajo = trabajo_id)
                now = timezone_now()
                now_date_string = '%s de %s de %s' % (now.day, MONTH_NAMES[now.month - 1], now.year)
                authors_emails = []
                authors_names = []
                for autor_trabajo in autores_trabajo:
                    authors_emails.append(autor_trabajo.autor.correo_electronico)
                    authors_names.append( autor_trabajo.autor.nombres.split(' ')[0] + ' ' + autor_trabajo.autor.apellidos.split(' ')[0] )
                
                instance_context = {
                    'recipient_name': '',
                    'roman_number': arbitraje.numero_romano,
                    'subject_title': autores_trabajo.first().trabajo.titulo_espanol,
                    'people_names': authors_names
                }
                instance_context.update(cert_context)
                certificate_gen = CertificateGenerator()
                certificate = certificate_gen.get_authors_certificate(instance_context)

                filename = "Certificado_Convencion_Asovac_%s.pdf" % (instance_context["roman_number"])

                context_email = {
                    'sistema': arbitraje,
                    'titulo_trabajo': autores_trabajo.first().trabajo.titulo_espanol,
                    'rol': 'autor'
                }
                msg_plain = render_to_string('../templates/email_templates/certificate.txt', context_email)
                msg_html = render_to_string('../templates/email_templates/certificate.html', context_email)

                email_msg = EmailMultiAlternatives('Certificado de autor(es)', msg_plain, config('EMAIL_HOST_USER'), authors_emails)
                email_msg.attach(filename, certificate.content, 'application/pdf')
                email_msg.attach_alternative(msg_html, "text/html")
                email_msg.send()

            messages.success(request, 'Se han enviado los certificados al(los) autor(es) seleccionados con éxito.')
            return redirect('recursos:resources_author')
    else:    
        form = CertificateToAuthorsForm(sistema_id = arbitraje_id)
    context = {
        'nombre_vista' : 'Recursos',
        'main_navbar_options' : TOP_NAVBAR_OPTIONS,
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'form': form
    }
    return render(request, 'recursos_author.html', context)



@login_required
def resources_referee(request):

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items
    if request.method == 'POST':
        form = CertificateToRefereeForm(request.POST, sistema_id = arbitraje.id)
        if form.is_valid():
            cert_context = create_certificate_context(arbitraje)
            for arbitro_id in form.cleaned_data['arbitros']:
                arbitro = Arbitro.objects.get(id = arbitro_id)
                now = timezone_now()
                now_date_string = '%s de %s de %s' % (now.day, MONTH_NAMES[now.month - 1], now.year)
                instance_context = {
                    'recipient_name': arbitro.nombres.split(' ')[0] + ' ' + arbitro.apellidos.split(' ')[0],
                    'roman_number': arbitraje.numero_romano,
                    'people_names': [arbitro.nombres.split(' ')[0] + ' ' + arbitro.apellidos.split(' ')[0]],
                    'peoples_id': arbitro.cedula_pasaporte
                }
                instance_context.update(cert_context)
                certificate_gen = CertificateGenerator()
                certificate = certificate_gen.get_referees_certificate(instance_context)

                name = instance_context["recipient_name"].split(' ')
                name = '_'.join(name)
                filename = "Certificado_%s_Convencion_Asovac_%s.pdf" % (name, instance_context["roman_number"])

                context_email = {
                    'sistema': arbitraje,
                    'usuario': arbitro.nombres.split(' ')[0] + ' ' + arbitro.apellidos.split(' ')[0],
                    'rol': 'árbitro de subárea'
                }
                msg_plain = render_to_string('../templates/email_templates/certificate.txt', context_email)
                msg_html = render_to_string('../templates/email_templates/certificate.html', context_email)

                email_msg = EmailMultiAlternatives('Certificado de árbitro', msg_plain, config('EMAIL_HOST_USER'), [arbitro.correo_electronico])
                email_msg.attach(filename, certificate.content, 'application/pdf')
                email_msg.attach_alternative(msg_html, "text/html")
                email_msg.send()

            messages.success(request, 'Se han enviado los certificados a los arbitros seleccionados con éxito.')
            return redirect('recursos:resources_referee')
    else:
        form = CertificateToRefereeForm(sistema_id = arbitraje.id)
    context = {
        'nombre_vista' : 'Recursos',
        'main_navbar_options' : TOP_NAVBAR_OPTIONS,
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'form': form,
    }
    return render(request, 'recursos_referee.html', context)



@login_required
def resources_event(request):
    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    return render(request, 'recursos_event_certificates.html', context)


@login_required
def create_logistics_certificates(request):
    form = MultipleRecipientsForm(request.POST or None)
    if request.method == 'POST':
        # Procesamiento manual del formulario
        recipients_tuples = list()
        n = 0
        while request.POST.get('recipients_name_' + str(n), None) or request.POST.get('recipients_email_' + str(n), None):
            name = request.POST.get('recipients_name_' + str(n), None).strip()
            email = request.POST.get('recipients_email_' + str(n), None).strip()
            recipients_tuples.append((name, email))
            n += 1
        # Validacion de campos vacios
        for r_name, r_email in recipients_tuples:
            if not (r_name and r_email):
                form.add_error(
                    None,
                    ValidationError(
                        "Todos los destinatarios deben poseer un nombre y correo electrónico asociados."
                    )
                )
                break

        print 'form error', form.errors
        if not form.errors:
            arbitraje_id = request.session['arbitraje_id']
            arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
            cert_context = create_certificate_context(arbitraje)
            certificate_gen = CertificateGenerator()
            for r_name, r_email in recipients_tuples:
                instance_context = {
                    "recipient_name": r_name,
                    "people_names": [r_name],
                }
                instance_context.update(cert_context)
                certificate = certificate_gen.get_logistics_certificate(instance_context)
                name = r_name.split(' ')
                name = '_'.join(name)
                filename = "CertificadoLogistica_%s_Convencion_Asovac_%s.pdf" % (name,
                                                                                 cert_context["roman_number"])
                context_email = {
                    'sistema': arbitraje,
                    'usuario': r_name,
                    'rol': 'miembro de la comisión de logística'
                }
                msg_plain = render_to_string('../templates/email_templates/generic_certificate.txt',
                                             context_email)
                msg_html = render_to_string('../templates/email_templates/generic_certificate.html',
                                            context_email)

                email_msg = EmailMultiAlternatives(
                    'Certificado de Comisión Logística',
                    msg_plain,
                    config('EMAIL_HOST_USER'),
                    [r_email]
                )
                email_msg.attach(filename, certificate.content, 'application/pdf')
                email_msg.attach_alternative(msg_html, "text/html")
                email_msg.send()

            messages.success(request, 'Se han enviado los certificados \
                a los destinatarios listados con éxito.')
            return redirect('recursos:create_logistics_certificates')

    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    context['form'] = form
    return render(request, 'recursos_event_logistics_certificate.html', context)



@login_required
def resources_sesion(request):
    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    return render(request, 'recursos_session_certificates.html', context)


@login_required
def create_session_coord_certificates(request):
    form = MultipleRecipientsForm(request.POST or None)
    if request.method == 'POST':
        # Procesamiento manual del formulario
        recipients_tuples = list()
        n = 0
        while request.POST.get('recipients_name_' + str(n), None) or request.POST.get('recipients_email_' + str(n), None):
            name = request.POST.get('recipients_name_' + str(n), None).strip()
            email = request.POST.get('recipients_email_' + str(n), None).strip()
            recipients_tuples.append((name, email))
            n += 1
        # Validacion de campos vacios
        for r_name, r_email in recipients_tuples:
            if not (r_name and r_email):
                form.add_error(
                    None,
                    ValidationError(
                        "Todos los destinatarios deben poseer un nombre y correo electrónico asociados."
                    )
                )
                break

        print 'form error', form.errors
        if not form.errors:
            arbitraje_id = request.session['arbitraje_id']
            arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
            cert_context = create_certificate_context(arbitraje)
            certificate_gen = CertificateGenerator()
            for r_name, r_email in recipients_tuples:
                instance_context = {
                    "recipient_name": r_name,
                    "people_names": [r_name],
                }
                instance_context.update(cert_context)
                certificate = certificate_gen.get_session_coord_certificate(instance_context)
                name = r_name.split(' ')
                name = '_'.join(name)
                filename = "CertificadoCoordinador_de_Sesion_Convencion_Asovac_%s.pdf" % cert_context["roman_number"]
                context_email = {
                    'sistema': arbitraje,
                    'usuario': r_name,
                    'rol': 'coordinador de sesión de presentación de trabajos libres'
                }
                msg_plain = render_to_string('../templates/email_templates/generic_certificate.txt',
                                             context_email)
                msg_html = render_to_string('../templates/email_templates/generic_certificate.html',
                                            context_email)

                email_msg = EmailMultiAlternatives(
                    'Certificado de Coordinador de Sesiones',
                    msg_plain,
                    config('EMAIL_HOST_USER'),
                    [r_email]
                )
                email_msg.attach(filename, certificate.content, 'application/pdf')
                email_msg.attach_alternative(msg_html, "text/html")
                email_msg.send()

            messages.success(request, 'Se han enviado los certificados \
                a los destinatarios listados con éxito.')
            return redirect('recursos:create_session_coord_certificates')

    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    context['form'] = form
    return render(request, 'recursos_session_coord_certificate.html', context)


@login_required
def resources_asovac(request):
    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    return render(request, 'recursos_asovac_documents.html', context)


@login_required
def create_organizer_comitee_certificates(request):
    form = MultipleRecipientsForm(request.POST or None)
    if request.method == 'POST':
        # Procesamiento manual del formulario
        recipients_tuples = list()
        n = 0
        while request.POST.get('recipients_name_' + str(n), None) or request.POST.get('recipients_email_' + str(n), None):
            name = request.POST.get('recipients_name_' + str(n), None).strip()
            email = request.POST.get('recipients_email_' + str(n), None).strip()
            recipients_tuples.append((name, email))
            n += 1
        # Validacion de campos vacios
        for r_name, r_email in recipients_tuples:
            if not (r_name and r_email):
                form.add_error(
                    None,
                    ValidationError(
                        "Todos los destinatarios deben poseer un nombre y correo electrónico asociados."
                    )
                )
                break

        print 'form error', form.errors
        if not form.errors:
            arbitraje_id = request.session['arbitraje_id']
            arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
            cert_context = create_certificate_context(arbitraje)
            certificate_gen = CertificateGenerator()
            for r_name, r_email in recipients_tuples:
                instance_context = {
                    "recipient_name": r_name,
                    "people_names": [r_name],
                }
                instance_context.update(cert_context)
                certificate = certificate_gen.get_comitee_certificate(instance_context)
                name = r_name.split(' ')
                name = '_'.join(name)
                filename = "CertificadoComite_Organizador_Convencion_Asovac_%s.pdf" % cert_context["roman_number"]
                context_email = {
                    'sistema': arbitraje,
                    'usuario': r_name,
                    'rol': 'miembro de la comisión organizadora'
                }
                msg_plain = render_to_string('../templates/email_templates/generic_certificate.txt',
                                             context_email)
                msg_html = render_to_string('../templates/email_templates/generic_certificate.html',
                                            context_email)

                email_msg = EmailMultiAlternatives(
                    'Certificado de Comisión Organizadora',
                    msg_plain,
                    config('EMAIL_HOST_USER'),
                    [r_email]
                )
                email_msg.attach(filename, certificate.content, 'application/pdf')
                email_msg.attach_alternative(msg_html, "text/html")
                email_msg.send()

            messages.success(request, 'Se han enviado los certificados \
                a los destinatarios listados con éxito.')
            return redirect('recursos:create_organizer_comitee_certificates')

    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    context['form'] = form
    return render(request, 'recursos_organizer_comitee_certificate.html', context)


@login_required
def resources_arbitration(request):

    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    return render(request, 'main_app_resources_arbitrations.html', context)


@login_required
def resources_paper(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
    # print (rol_id)
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
    # print items
    if request.method == "POST":
        form = CertificateToAuthorsForm(request.POST, sistema_id = arbitraje_id)
        if form.is_valid():
            cert_context = create_certificate_context(arbitraje)
            for trabajo_id in form.cleaned_data['trabajos']:
                autores_trabajo = Autores_trabajos.objects.filter(trabajo = trabajo_id)
                """
                - context["subject_title"] = String que representa el nombre del trabajo certificado.
                - context["people_names"] = Lista de Strings con los nombres de los autores del trabajo.
                - context["roman_number"] = Numero romano de la convencion
                """
                now = timezone_now()
                now_date_string = '%s de %s de %s' % (now.day, MONTH_NAMES[now.month - 1], now.year)
                authors_emails = []
                authors_names = []
                for autor_trabajo in autores_trabajo:
                    authors_emails.append(autor_trabajo.autor.correo_electronico)
                    authors_names.append( autor_trabajo.autor.nombres.split(' ')[0] + ' ' + autor_trabajo.autor.apellidos.split(' ')[0] )
                
                instance_context = {
                    'roman_number': arbitraje.numero_romano,
                    'people_names': authors_names,
                    'subject_title': autores_trabajo.first().trabajo.titulo_espanol,
                }
                instance_context.update(cert_context)
                certificate_gen = CertificateGenerator()
                certificate = certificate_gen.get_paper_certificate(instance_context)

                filename = "Certificado_%s_Convencion_Asovac_%s.pdf" % (instance_context["subject_title"],instance_context["roman_number"])

                context_email = {
                    'sistema': arbitraje,
                    'titulo_trabajo': autores_trabajo.first().trabajo.titulo_espanol,
                    'rol': 'autor'
                }
                msg_plain = render_to_string('../templates/email_templates/certificate.txt', context_email)
                msg_html = render_to_string('../templates/email_templates/certificate.html', context_email)

                email_msg = EmailMultiAlternatives('Certificado por trabajo', msg_plain, config('EMAIL_HOST_USER'), authors_emails)
                email_msg.attach(filename, certificate.content, 'application/pdf')
                email_msg.attach_alternative(msg_html, "text/html")
                email_msg.send()

            messages.success(request, 'Se han enviado los certificados de los trabajos seleccionados al(los) autor(es) con éxito.')
            return redirect('recursos:resources_paper')
    else:    
        form = CertificateToAuthorsForm(sistema_id = arbitraje_id)
    context = {
        'nombre_vista' : 'Recursos',
        'main_navbar_options' : main_navbar_options,
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'form': form,
        'paper': True, 
    }
    return render(request, 'recursos_author.html', context)
