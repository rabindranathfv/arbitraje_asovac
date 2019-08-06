# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now as timezone_now

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from autores.models import Autores_trabajos, Autor

from main_app.models import Usuario_rol_in_sistema, Rol, Sistema_asovac, Usuario_asovac
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status

from trabajos.models import Trabajo_arbitro

from .utils import CertificateGenerator, LetterGenerator#, generate_authors_certificate

MONTH_NAMES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
               'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

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
    context["recipient_name"] = 'Rabindranath Ferreira'
    context["city"] = 'Caracas'
    context["header_url"] = arbitraje.cabecera
    context["authority1_info"] = arbitraje.autoridad1.replace(',', '<br/>')
    context["signature1_path"] = os.path.join(os.path.join(settings.MEDIA_ROOT), path1)
    context["authority2_info"] = arbitraje.autoridad2.replace(',', '<br/>')
    context["signature2_path"] = os.path.join(os.path.join(settings.MEDIA_ROOT), path2)
    context["logo_path"] = os.path.join(os.path.join(settings.MEDIA_ROOT), path_logo)
    context['date_string'] = now_date_string
    context["roman_number"] = 'LXVII'
    context["subject_title"] = 'Comisión Organizadora de la LXVII Convencion Anual AsoVAC'
    context["people_names"] = ['Rabindranath Ferreira']
    context["peoples_id"] = 'V-6.186.871'

    return context


def abreviate_if_neccesary(area_nombre):
    nombre_abreviado = ""
    if (len(area_nombre) > 20):
        for item in area_nombre.split(" "):
            if item[0].isupper():
                nombre_abreviado += item[0]
        return nombre_abreviado
    else:
        return area_nombre


# Create your views here.
@login_required
def recursos_pag(request):
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
    }
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

    return certificate_gen.get_comitee_certificate(context)


@login_required
def resources_author(request):
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
    }
    return render(request, 'main_app_resources_author.html', context)



@login_required
def resources_referee(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]



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
    }
    return render(request, 'main_app_resources_referee.html', context)



@login_required
def resources_event(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


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
    }
    return render(request, 'main_app_resources_event.html', context)



@login_required
def resources_sesion(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


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
    }
    return render(request, 'main_app_resources_sesion.html', context)



@login_required
def resources_asovac(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


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
    }
    return render(request, 'main_app_resources_asovac.html', context)



@login_required
def resources_arbitration(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


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
    }
    return render(request, 'main_app_resources_arbitrations.html', context)

