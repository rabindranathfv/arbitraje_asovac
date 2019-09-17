# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, re, random, string,xlrd,sys,xlwt
from openpyxl import Workbook
import datetime
from decouple import config

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.forms import ValidationError
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render,redirect, reverse
from django.template.loader import render_to_string
from django.utils.timezone import now as timezone_now

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .guards import *

from arbitrajes.models import Arbitro
from autores.forms import ImportFromExcelForm
from autores.models import Autores_trabajos, Autor
from autores.views import get_extension_file, validate_alpha
from main_app.forms import UploadFileForm
from main_app.models import Usuario_rol_in_sistema, Sistema_asovac, Area
from main_app.views import (
    get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar,
    get_roles, get_route_configuracion, get_route_seguimiento,
    validate_rol_status, handle_uploaded_file
)
from main_app.decorators import user_is_arbitraje
from trabajos.models import Trabajo_arbitro

from .utils import (
    CertificateGenerator, MiscellaneousGenerator, validate_recipients_excel
)
from .forms import (
    CertificateToRefereeForm, CertificateToAuthorsForm, MultipleRecipientsForm,
    MultipleRecipientsWithDateForm, MultipleRecipientsWithDateAndSubjectForm,
    MultipleRecipientsWithRoleForm
)


MONTH_NAMES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
               'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

TOP_NAVBAR_OPTIONS = [{'title':'Configuración', 'icon': 'fa-cogs', 'active': True},
                      {'title':'Monitoreo', 'icon': 'fa-eye', 'active': False},
                      {'title':'Resultados', 'icon': 'fa-chart-area','active': False},
                      {'title':'Administración', 'icon': 'fa-archive', 'active': False}]

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
    date_start_string = '%s de %s' % (arbitraje.fecha_inicio_arbitraje.day,
                                      MONTH_NAMES[arbitraje.fecha_inicio_arbitraje.month - 1])
    date_end_string = '%s de %s de %s' % (arbitraje.fecha_fin_arbitraje.day,
                                          MONTH_NAMES[arbitraje.fecha_fin_arbitraje.month - 1],
                                          arbitraje.fecha_fin_arbitraje.year)
    university_names = arbitraje.sedes.split(',')
    university_names = map(lambda n: n.strip(), university_names)
    print university_names
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
    context["date_start_string"] = date_start_string
    context["date_end_string"] = date_end_string
    context["university_names"] = university_names

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
@user_is_arbitraje
def recursos_pag(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id = get_roles(request.user.id, arbitraje_id)
    if not resultados_guard(estado, rol_id):
        raise PermissionDenied
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
@user_is_arbitraje
def generate_pdf(request,*args , **kwargs):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    start_date = arbitraje.fecha_inicio_arbitraje
    end_date = arbitraje.fecha_fin_arbitraje
    date_start_string = '%s de %s' % (start_date.day, MONTH_NAMES[start_date.month - 1])
    date_end_string = '%s de %s de %s' % (end_date.day, MONTH_NAMES[end_date.month - 1], end_date.year)

    filename = "AsoVAC_Rabindranath_Ferreira.pdf"

    context = {}
    context["date_start_string"] = date_start_string
    context["date_end_string"] = date_end_string
    context["university_names"] = ['Universidad Metropolitana', 'Universidad Central de Venezuela']
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
    context["subject_title"] = 'Rabindranath Ferreira Villamizar'
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
    doc_gen = MiscellaneousGenerator()

    return doc_gen.get_name_tag(filename, context)


@login_required
@user_is_arbitraje
def create_approval_letters(request):
    pass


@login_required
@user_is_arbitraje
def create_authors_certificates(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)

    context = create_certificate_context(arbitraje)

    certificate_gen = CertificateGenerator()

    return certificate_gen.get_authors_certificate(context)


@login_required
@user_is_arbitraje
def resources_author(request):

    # print (rol_id)
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)
    
    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

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
        'form': form,
        'admin_styles': True
    }
    return render(request, 'recursos_author.html', context)


@login_required
@user_is_arbitraje
def resources_referee(request):

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

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
        'admin_styles': True
    }

    return render(request, 'recursos_referee.html', context)


@login_required
@user_is_arbitraje
def resources_event(request):
    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    return render(request, 'recursos_event_certificates.html', context)


@login_required
@user_is_arbitraje
def create_logistics_certificates(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

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
        if len(recipients_tuples) <= 0:
            form.add_error(
                None,
                ValidationError(
                    "Por favor ingrese al menos un nombre y un correo electrónico."
                )
            )

        for r_name, r_email in recipients_tuples:
            print 'VALIDANDO TUPLAS'
            print r_name
            print r_email
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
@user_is_arbitraje
def resources_sesion(request):
    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    return render(request, 'recursos_session_certificates.html', context)


@login_required
@user_is_arbitraje
def create_session_coord_certificates(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

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
        if len(recipients_tuples) <= 0:
            form.add_error(
                None,
                ValidationError(
                    "Por favor ingrese al menos un nombre y un correo electrónico."
                )
            )
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
@user_is_arbitraje
def resources_asovac(request):
    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    return render(request, 'recursos_asovac_documents.html', context)


@login_required
@user_is_arbitraje
def create_organizer_comitee_certificates(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

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
        if len(recipients_tuples) <= 0:
            form.add_error(
                None,
                ValidationError(
                    "Por favor ingrese al menos un nombre y un correo electrónico."
                )
            )
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
@user_is_arbitraje
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

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

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
        'admin_styles': True
    }
    return render(request, 'recursos_author.html', context)


@login_required
@user_is_arbitraje
def create_name_tags(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

    form = MultipleRecipientsWithRoleForm(request.POST or None)
    context = create_common_context(request)
    if request.method == 'POST':
        if form.is_valid():
            # Procesamiento manual del formulario
            recipients_tuples = list()
            n = 0
            while request.POST.get('recipients_name_' + str(n), None) or request.POST.get('recipients_email_' + str(n), None):
                name = request.POST.get('recipients_name_' + str(n), None).strip()
                email = request.POST.get('recipients_email_' + str(n), None).strip()
                recipients_tuples.append((name, email))
                n += 1

            # Validacion de campos vacios
            if len(recipients_tuples) <= 0:
                form.add_error(
                    None,
                    ValidationError(
                        "Por favor ingrese al menos un nombre y un correo electrónico."
                    )
                )
            for r_name, r_email in recipients_tuples:
                if not (r_name and r_email):
                    form.add_error(
                        None,
                        ValidationError(
                            "Todos los destinatarios deben poseer un nombre y correo electrónico asociados."
                        )
                    )
                    break

            if not form.errors and form.is_valid():
                role = form.cleaned_data['role']
                arbitraje_id = request.session['arbitraje_id']
                arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
                nametag_context = create_certificate_context(arbitraje)
                misc_gen = MiscellaneousGenerator()
                for r_name, r_email in recipients_tuples:
                    instance_context = {
                        'subject_title': r_name,
                        'role': role.capitalize(),
                    }
                    filename = "Portanombre AsoVAC.pdf"
                    instance_context.update(nametag_context)
                    certificate = misc_gen.get_name_tag(filename, instance_context)

                    context_email = {
                        'sistema': arbitraje,
                        'usuario': r_name,
                        'rol': role.capitalize()
                    }
                    msg_plain = render_to_string('../templates/email_templates/nametag.txt',
                                                 context_email)
                    msg_html = render_to_string('../templates/email_templates/nametag.html',
                                                context_email)

                    email_msg = EmailMultiAlternatives(
                        'Portanombre AsoVAC',
                        msg_plain,
                        config('EMAIL_HOST_USER'),
                        [r_email]
                    )
                    email_msg.attach(filename, certificate.content, 'application/pdf')
                    email_msg.attach_alternative(msg_html, "text/html")
                    email_msg.send()
                    print '1 EMAIL ENVIADO A:'
                    print email

                messages.success(request, 'Se han generado y enviado los portanombres con éxito')
                return redirect('recursos:create_name_tags')

    context['nombre_vista'] = 'Generación de Portanombres'
    context['form'] = form
    return render(request, 'recursos_create_nametags.html', context)


@login_required
@user_is_arbitraje
def resources_organizer(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

    form = MultipleRecipientsWithDateForm(request.POST or None)
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
        if len(recipients_tuples) <= 0:
            form.add_error(
                None,
                ValidationError(
                    "Por favor ingrese al menos un nombre y un correo electrónico."
                )
            )
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
        if not form.errors and form.is_valid():
            fecha_evento = form.cleaned_data['recipients_date']
            nombre_evento = form.cleaned_data['recipients_event_name']
            arbitraje_id = request.session['arbitraje_id']
            arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
            cert_context = create_certificate_context(arbitraje)
            certificate_gen = CertificateGenerator()
            for r_name, r_email in recipients_tuples:
                instance_context = {
                    "subject_title": nombre_evento,
                    "people_names": [r_name],
                    "event_name_string": nombre_evento,
                    "event_date_string": fecha_evento.strftime('%d/%m/%Y')

                }
                instance_context.update(cert_context)
                certificate = certificate_gen.get_organizer_certificate(instance_context)
                name = r_name.split(' ')
                name = '_'.join(name)
                filename = "Certificado_Organizadores_%s_Convencion_Asovac_%s.pdf" % (name,
                                                                                 cert_context["roman_number"])
                context_email = {
                    'sistema': arbitraje,
                    'usuario': r_name,
                    'rol': 'organizador'
                }
                msg_plain = render_to_string('../templates/email_templates/generic_certificate.txt',
                                             context_email)
                msg_html = render_to_string('../templates/email_templates/generic_certificate.html',
                                            context_email)

                email_msg = EmailMultiAlternatives(
                    'Certificado de organizador',
                    msg_plain,
                    config('EMAIL_HOST_USER'),
                    [r_email]
                )
                email_msg.attach(filename, certificate.content, 'application/pdf')
                email_msg.attach_alternative(msg_html, "text/html")
                email_msg.send()

            messages.success(request, 'Se han enviado los certificados \
                a los destinatarios listados con éxito.')
            return redirect('recursos:resources_organizer')

    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    context['form'] = form
    context['conferencista'] = 0
    context['url_modal'] = reverse('recursos:load_organizers_modal')
    return render(request, 'recursos_organizer_certificate.html', context)


@login_required
@user_is_arbitraje
def resources_lecturer(request):
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

    form = MultipleRecipientsWithDateAndSubjectForm(request.POST or None)
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
        if len(recipients_tuples) <= 0:
            form.add_error(
                None,
                ValidationError(
                    "Por favor ingrese al menos un nombre y un correo electrónico."
                )
            )

        for r_name, r_email in recipients_tuples:
            if not (r_name and r_email):
                form.add_error(
                    None,
                    ValidationError(
                        "Todos los destinatarios deben poseer un nombre y correo electrónico asociados."
                    )
                )
                break
        if n == 0:
            form.add_error(
                None,
                ValidationError(
                    "Se requiere al menos un destinatario, por favor indique el nombre y el correo electrónico."
                )
            )
        # print 'form error', form.errors
        if not form.errors and form.is_valid():
            fecha_evento = form.cleaned_data['recipients_date']
            nombre_evento = form.cleaned_data['recipients_event_name']
            titulo_conferencia = form.cleaned_data['recipients_conference_name']
            arbitraje_id = request.session['arbitraje_id']
            arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
            cert_context = create_certificate_context(arbitraje)
            certificate_gen = CertificateGenerator()
            for r_name, r_email in recipients_tuples:
                instance_context = {
                    "subject_title": titulo_conferencia,
                    "people_names": [r_name],
                    "event_name_string": nombre_evento,
                    "event_date_string": fecha_evento.strftime('%d/%m/%Y')

                }
                instance_context.update(cert_context)
                certificate = certificate_gen.get_lecturer_certificate(instance_context)
                name = r_name.split(' ')
                name = '_'.join(name)
                filename = "Certificado_Conferencia_%s_Convencion_Asovac_%s.pdf" % (name,
                                                                                 cert_context["roman_number"])
                context_email = {
                    'sistema': arbitraje,
                    'usuario': r_name,
                    'rol': 'conferencista'
                }
                msg_plain = render_to_string('../templates/email_templates/generic_certificate.txt',
                                             context_email)
                msg_html = render_to_string('../templates/email_templates/generic_certificate.html',
                                            context_email)

                email_msg = EmailMultiAlternatives(
                    'Certificado de conferencista',
                    msg_plain,
                    config('EMAIL_HOST_USER'),
                    [r_email]
                )
                email_msg.attach(filename, certificate.content, 'application/pdf')
                email_msg.attach_alternative(msg_html, "text/html")
                email_msg.send()

            messages.success(request, 'Se han enviado los certificados \
                a los destinatarios listados con éxito.')
            return redirect('recursos:resources_lecturer')

    context = create_common_context(request)
    context['nombre_vista'] = 'Recursos'
    context['form'] = form
    context['conferencista'] = 1
    context['url_modal'] = reverse('recursos:load_lecturers_modal')
    return render(request, 'recursos_organizer_certificate.html', context)

#---------------------------------------------------------------------------------#
#                Guarda el archivo en la carpeta del proyecto                     #
#---------------------------------------------------------------------------------#
def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    # print "Nombre del archivo a guardar: ",filename
    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

@login_required
@user_is_arbitraje
# Para guardar el archivo recibido del formulario
def save_file(request,type_load):

    name= str(request.FILES.get('file'))

    extension = name.split('.')
    file_name= "carga"+ type_load +"."+extension[1]
    # Permite guardar el archivo y asignarle un nombre
    handle_uploaded_file(request.FILES['file'], file_name)
    route= "upload/"+file_name
    # print "Ruta del archivo: ",route
    return route

@login_required
@user_is_arbitraje
def load_lecturers_modal(request):
    data = dict()
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

    if request.method == "POST":
        form = ImportFromExcelForm(request.POST, request.FILES)
        if form.is_valid():
			# Para guardar el archivo de forma local
            file_name= save_file(request,"conferencistas")
            extension= get_extension_file(file_name)

            #Valida el contenido del archivo
            response = validate_load_event_participants(file_name, extension,arbitraje_id, True)
            print response
            if response['status'] == 200:
                context = {
                    'title': 'Cargar Conferencistas',
                    'response': response['message'],
                    'status': response['status'],
                }
                print (response['message'], response['status'])
                data['html_form'] = render_to_string('ajax/modal_succes.html', context, request=request)
                return JsonResponse(data)
            
            else:
				messages.error(request, response['message'])


			#data['url'] = reverse('autores:authors_list')
			#data['form_is_valid'] = True
        else:       
			#data['form_is_valid'] = False
			messages.error(request, "El archivo indicado no es xls o xlsx, por favor suba un archivo en alguno de esos dos formatos.")

    else:
		form = ImportFromExcelForm()

    context = {
		'form': form,
		'rol': 'conferencistas',
		'action': reverse('recursos:load_lecturers_modal'),
        'format_url': reverse('recursos:format_import_participants', kwargs={ 'option': 2})
	}
    data['html_form'] = render_to_string('ajax/load_excel.html', context, request=request)
    return JsonResponse(data)


@login_required
@user_is_arbitraje
def load_organizers_modal(request):
    data = dict()
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied

    if request.method == "POST":
        form = ImportFromExcelForm(request.POST, request.FILES)
        if form.is_valid():
			# Para guardar el archivo de forma local
            file_name= save_file(request,"organizadores")
            extension= get_extension_file(file_name)

            #Valida el contenido del archivo
            response = validate_load_event_participants(file_name, extension,arbitraje_id)
            print response

            if response['status'] == 200:
                context = {
                    'title': 'Cargar Organizadores',
                    'response': response['message'],
                    'status': response['status'],
                }
                print (response['message'], response['status'])
                data['html_form'] = render_to_string('ajax/modal_succes.html', context, request=request)
                return JsonResponse(data)

            else:
				messages.error(request, response['message'])

			#data['url'] = reverse('autores:authors_list')
			#data['form_is_valid'] = True
        else:
			#data['form_is_valid'] = False
			messages.error(request, "El archivo indicado no es xls o xlsx, por favor suba un archivo en alguno de esos dos formatos.")

    else:
		form = ImportFromExcelForm()

    context ={
		'form': form,
		'rol': 'organizadores',
		'action': reverse('recursos:load_organizers_modal'),
        'format_url': reverse('recursos:format_import_participants', kwargs={ 'option': 1})
	}
    data['html_form'] = render_to_string('ajax/load_excel.html', context, request=request)
    return JsonResponse(data)


@login_required
@user_is_arbitraje
def load_nametag_recipients_modal(request):
    data = dict()
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id , arbitraje_id)

    if not recursos_guard(estado, rol_id):
        raise PermissionDenied
        
    form = UploadFileForm(request.POST or None, request.FILES or None)
    context = create_common_context(request)
    response_context = {'title': 'Carga Destinatarios de Portanombres'}
    if request.method == "POST":
        if form.is_valid():
            extension = str(request.FILES.get('file')).decode('UTF-8').split('.')[-1]
            filename = "destinatarios_portanombre." + extension
            handle_uploaded_file(request.FILES['file'], filename)
            filename = 'upload/' + filename

            arbitraje_id = request.session['arbitraje_id']
            arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
            nametag_context = create_certificate_context(arbitraje)

            response = validate_recipients_excel(filename, extension)

            if response['status'] == 400:
                # Se regreso algun codigo de error?
                response_context['response'] = response['message']
                response_context['status'] = 400
                data['html_form'] = render_to_string('ajax/modal_succes.html', response_context, request=request)
                return JsonResponse(data)

            sheet = xlrd.open_workbook(filename).sheet_by_index(0)
            pdf_filename = 'Portanombre_AsoVAC.pdf'
            nametag_gen = MiscellaneousGenerator()

            for fila in range(1, sheet.nrows):
                try:
                    full_name = sheet.cell_value(rowx=fila, colx=0).strip()
                    role = sheet.cell_value(rowx=fila, colx=1).strip().lower()
                    email = sheet.cell_value(rowx=fila, colx=2).strip()
                except:
                    response_context['response'] = "Ha ocurrido un error con los parámetros recibidos, vuelva a intentar."
                    response_context['status'] = 400
                    data['html_form'] = render_to_string('ajax/modal_succes.html', response_context, request=request)
                    return JsonResponse(data)

                role = role.capitalize()
                instance_context = {
                    'subject_title': full_name,
                    'role': role,
                }
                instance_context.update(nametag_context)
                nametag = nametag_gen.get_name_tag(pdf_filename, instance_context)
                context_email = {
                    'sistema': arbitraje,
                    'usuario': full_name,
                    'rol': role,
                }
                msg_plain = render_to_string('email_templates/nametag.txt', context_email)
                msg_html = render_to_string('email_templates/nametag.html', context_email)

                email_msg = EmailMultiAlternatives(
                    'Portanombre AsoVAC',
                    msg_plain,
                    config('EMAIL_HOST_USER'),
                    [email]
                )
                email_msg.attach(pdf_filename, nametag.content, 'application/pdf')
                email_msg.attach_alternative(msg_html, "text/html")
                email_msg.send()
            response_context['response'] = response['message']
            response_context['status'] = response['status']
            data['html_form'] = render_to_string('ajax/modal_succes.html', response_context, request=request)
            return JsonResponse(data)
        else:
            response_context['response'] = "El archivo indicado no es xls o xlsx, por favor suba un archivo en alguno de esos dos formatos."
            response_context['status'] = 400
            data['html_form'] = render_to_string('ajax/modal_succes.html', response_context, request=request)
            return JsonResponse(data)


    context['form'] = form
    context = {
        'form': form,
        'rol': 'destinatarios de portanombres',
        'action': reverse('recursos:load_nametag_recipients_modal'),
        'format_url': reverse('recursos:format_nametag_recipients')
    }
    data['html_form'] = render_to_string('ajax/load_excel.html', context, request=request)
    return JsonResponse(data)


def validate_load_event_participants(filename,extension,arbitraje_id, lecturer = False):
    data= dict()
    data['status']=400
    data['message']="La estructura del archivo no es correcta"
    if lecturer:
        ncols = 5
    else:
        ncols = 4
    if extension == "xlsx" or extension == "xls":
        book = xlrd.open_workbook(filename)
        if book.nsheets > 0:
            excel_file = book.sheet_by_index(0)
            email_pattern = re.compile('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')

            if excel_file.ncols == ncols:
                data['status']=200
                data['message']=""
                # se validan los campos del documento
                for fila in range(excel_file.nrows):
                    # Para no buscar los titulos
                    if fila > 0:
                        if excel_file.cell_value(rowx=fila, colx=0) == '':
							data['status']=400
							data['message'] = "Error en la fila {0} el nombre del evento es un campo obligatorio \n".format(fila)
                        

                        if excel_file.cell_value(rowx=fila, colx=1) == '':
							data['status']=400
							data['message'] = "Error en la fila {0} la fecha del evento es un campo obligatorio \n".format(fila)
                        else:
                            
                            try:
                                year, month, day, hour, minute, second = xlrd.xldate_as_tuple(excel_file.cell_value(rowx=fila, colx=1), book.datemode)
                            except:
                                data['status']=400
                                data['message'] = "Error en la fila {0} la fecha debe tener formato dd/mm/AAAA \n".format(fila)
                        
                        if excel_file.cell_value(rowx=fila, colx=2) == '':
							data['status']=400
							data['message'] = "Error en la fila {0} el correo electrónico del destinatario es un campo obligatorio \n".format(fila)
                        elif not email_pattern.match(excel_file.cell_value(rowx=fila, colx=2).strip()):
                            data['status']=400
                            data['message'] = "Error en la fila {0} el correo electrónico del destinatario no tiene un formato correcto \n".format(fila)
                        
                        if excel_file.cell_value(rowx=fila, colx=3) == '':
							data['status']=400
							data['message'] = "Error en la fila {0} el nombre del destinatario es un campo obligatorio \n".format(fila)
                        else:
							nombres_is_valid = validate_alpha(str(excel_file.cell_value(rowx=fila, colx=3)).strip())
							if not nombres_is_valid:
								data['status']=400
								data['message'] = "Error en la fila {0} el campo de nombre del destinatario, solo debe tener letras \n".format(fila)
                        
                        if lecturer:
                            if excel_file.cell_value(rowx=fila, colx=4) == '':
                                data['status']=400
                                data['message'] = "Error en la fila {0} el título de la conferencia es un campo obligatorio \n".format(fila)
    if data['status'] == 200:
        if lecturer:
            generate_massive_lecturers_certificates(book, arbitraje_id)
        else:
            generate_massive_organizer_certificates(book, arbitraje_id)
        data['message'] = "Se han generado y envíado los certificados con éxito"
        book.release_resources()
        del book
    print(data)
    return data


def generate_massive_lecturers_certificates(book, arbitraje_id):
    arbitraje = Sistema_asovac.objects.get(id = arbitraje_id)
    cert_context = create_certificate_context(arbitraje)
    certificate_gen = CertificateGenerator()
    excel_file = book.sheet_by_index(0)
    for fila in range(excel_file.nrows):
        if fila > 0:
            
            nombre_evento = excel_file.cell_value(rowx=fila, colx=0)
            year, month, day, hour, minute, second = xlrd.xldate_as_tuple(excel_file.cell_value(rowx=fila, colx=1), book.datemode)
            email = excel_file.cell_value(rowx=fila, colx=2)
            nombre = excel_file.cell_value(rowx=fila, colx=3)
            titulo_conferencia = excel_file.cell_value(rowx=fila, colx=4)
            if day < 10:
                day = '0'+ str(day)
            else:
                day = str(day)

            if month < 10:
                month = '0'+ str(month)
            else:
                month = str(month)

            instance_context = {
                "subject_title": titulo_conferencia,
                "people_names": [nombre],
                "event_name_string": nombre_evento,
                "event_date_string": day + '/'+ month +'/'+str(year)

            }
            instance_context.update(cert_context)
            certificate = certificate_gen.get_lecturer_certificate(instance_context)
            name = nombre.split(' ')
            name = '_'.join(name)
            filename = "Certificado_Conferencia_%s_Convencion_Asovac_%s.pdf" % (name,
                                                                                cert_context["roman_number"])
            context_email = {
                'sistema': arbitraje,
                'usuario': nombre,
                'rol': 'conferencista'
            }
            msg_plain = render_to_string('../templates/email_templates/generic_certificate.txt',
                                            context_email)
            msg_html = render_to_string('../templates/email_templates/generic_certificate.html',
                                        context_email)

            email_msg = EmailMultiAlternatives(
                'Certificado de conferencista',
                msg_plain,
                config('EMAIL_HOST_USER'),
                [email]
            )
            email_msg.attach(filename, certificate.content, 'application/pdf')
            email_msg.attach_alternative(msg_html, "text/html")
            email_msg.send()


def generate_massive_organizer_certificates(book, arbitraje_id):
    resultado = True
    arbitraje = Sistema_asovac.objects.get(id = arbitraje_id)
    cert_context = create_certificate_context(arbitraje)
    certificate_gen = CertificateGenerator()
    excel_file = book.sheet_by_index(0)
    for fila in range(excel_file.nrows):
        if fila > 0:
            
            nombre_evento = excel_file.cell_value(rowx=fila, colx=0)
            year, month, day, hour, minute, second = xlrd.xldate_as_tuple(excel_file.cell_value(rowx=fila, colx=1), book.datemode)
            email = excel_file.cell_value(rowx=fila, colx=2)
            nombre = excel_file.cell_value(rowx=fila, colx=3)

            if day < 10:
                day = '0'+ str(day)
            else:
                day = str(day)

            if month < 10:
                month = '0'+ str(month)
            else:
                month = str(month)

            instance_context = {
                "subject_title": nombre_evento,
                "people_names": [nombre],
                "event_name_string": nombre_evento,
                "event_date_string": day + '/' + month + '/' + str(year)

            }
            instance_context.update(cert_context)
            certificate = certificate_gen.get_organizer_certificate(instance_context)
            name = nombre_evento.split(' ')
            name = '_'.join(name)
            filename = "Certificado_Organizadores_%s_Convencion_Asovac_%s.pdf" % (name,
                                                                                cert_context["roman_number"])
            context_email = {
                'sistema': arbitraje,
                'usuario': nombre_evento,
                'rol': 'organizador'
            }
            msg_plain = render_to_string('../templates/email_templates/generic_certificate.txt',
                                            context_email)
            msg_html = render_to_string('../templates/email_templates/generic_certificate.html',
                                        context_email)

            email_msg = EmailMultiAlternatives(
                'Certificado de organizador',
                msg_plain,
                config('EMAIL_HOST_USER'),
                [email]
            )
            email_msg.attach(filename, certificate.content, 'application/pdf')
            email_msg.attach_alternative(msg_html, "text/html")
            email_msg.send()


@login_required
@user_is_arbitraje
def format_import_participants(request, option):

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(id=arbitraje_id)
    data = []
    # Para definir propiedades del documento de excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=convencion_asovac_{0}_formato_conferencistas.xls'.format(arbitraje.fecha_inicio_arbitraje.year)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("Conferencistas")
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    # Para agregar los titulos de cada columna
    row_num = 0
    columns = ['Nombre Evento(*)', 'Fecha Evento(*)']
    if option == '2':
        columns.append('Correo electrónico del conferencista(*)')
        columns.append('Nombre Completo del Conferencista(*)')
        columns.append('Título de conferencia(*)')
    else:
        columns.append('Correo electrónico del organizador(*)')
        columns.append('Nombre Completo del Organizador(*)')

    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])

    row_num += 1
    columns = ['Evento 1', 'Fecha', 'juanito@email.com', 'Juanito Perez']
    if option == '2':
        columns.append('Título 1')
        print(columns)

    for col_num in range(len(columns)):
        if col_num != 1:
		    worksheet.write(row_num, col_num, columns[col_num])
        else:
            worksheet.write(row_num, col_num, datetime.datetime.strptime("01/01/2019", "%d/%M/%Y").date(), date_format)

    row_num += 1
    columns = ['Evento 2',  'Fecha', 'juanita@email.com', 'Juanita Perez']
    if option == '2':
        columns.append('Título 2')
    for col_num in range(len(columns)):
        if col_num != 1:
		    worksheet.write(row_num, col_num, columns[col_num])
        else:
            worksheet.write(row_num, col_num, datetime.datetime.strptime("29/10/2019", "%d/%M/%Y").date() , date_format)

    workbook.save(response)
    return response


@login_required
@user_is_arbitraje
def format_nametag_recipients(request):
    # Para definir propiedades del documento de excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=convencion_asovac_formato_portanombres.xls'
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet("Destinatarios")

    # Para agregar los titulos de cada columna
    row_num = 0
    columns = ['Nombre Completo(*)', 'Rol(*)', 'Correo electrónico(*)'] 
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])

    row_num += 1
    columns = ['Juanito Perez', 'conferencista', 'juanito@email.com']
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])

    row_num += 1
    columns = ['Juanita Perez', 'asistente', 'juanita@email.com', ]
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])

    row_num += 1
    columns = ['Juan Perez', 'autor', 'juan@email.com', ]
    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num])

    workbook.save(response)
    return response
