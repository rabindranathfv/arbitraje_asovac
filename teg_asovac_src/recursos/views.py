# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.template.loader import get_template

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from arbitrajes.models import Arbitraje
from autores.models import Autores_trabajos, Autor
from main_app.models import Usuario_rol_in_sistema, Rol, Sistema_asovac, Usuario_asovac
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status
from trabajos.models import Trabajo, Trabajo_arbitro

from .utils import generate_acceptation_letter, generate_acceptation_letter_with_observations, generate_rejection_letter_with_observations

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
        
        sociedad_fisica_aceptados = 0
        sociedad_fisica_rechazados = 0
        ciencias_sociales_aceptados = 0
        ciencias_sociales_rechazados = 0
        tecnologia_aceptados = 0
        tecnologia_rechazados = 0
        ciencias_exactas_aceptados = 0
        ciencias_exactas_rechazados = 0
        biociencias_aceptados = 0
        biociencias_rechazados = 0

        autores_sociedad_fisica = []
        autores_ciencias_sociales = []
        autores_tecnologia = []
        autores_ciencias_exactas = []
        autores_biociencias = []

        for autor_trabajo in autores_trabajos:
            if autor_trabajo.es_autor_principal:    
                invitaciones_aceptadas += Trabajo_arbitro.objects.filter(trabajo = autor_trabajo.trabajo, invitacion = True).count()
                invitaciones_pendientes += Trabajo_arbitro.objects.filter(trabajo = autor_trabajo.trabajo, invitacion = False, fin_arbitraje = False).count()
            if autor_trabajo.trabajo.subareas.first().area.id == 1:
                if not autor_trabajo.autor.id in autores_biociencias:
                    autores_biociencias.append(autor_trabajo.autor.id)

                if autor_trabajo.trabajo.estatus == "Aceptado" and autor_trabajo.es_autor_principal:
                    biociencias_aceptados += 1
                elif autor_trabajo.trabajo.estatus == "Rechazado" and autor_trabajo.es_autor_principal:
                    biociencias_rechazados += 1
            elif autor_trabajo.trabajo.subareas.first().area.id == 2:
                if not autor_trabajo.autor.id in autores_ciencias_exactas:
                    autores_ciencias_exactas.append(autor_trabajo.autor.id)

                if autor_trabajo.trabajo.estatus == "Aceptado" and autor_trabajo.es_autor_principal:
                    ciencias_exactas_aceptados += 1
                elif autor_trabajo.trabajo.estatus == "Rechazado" and autor_trabajo.es_autor_principal: 
                    ciencias_exactas_rechazados += 1
            elif autor_trabajo.trabajo.subareas.first().area.id == 3:
                if not autor_trabajo.autor.id in autores_tecnologia:
                    autores_tecnologia.append(autor_trabajo.autor.id)

                if autor_trabajo.trabajo.estatus == "Aceptado" and autor_trabajo.es_autor_principal:
                    tecnologia_aceptados += 1
                elif autor_trabajo.trabajo.estatus == "Rechazado" and autor_trabajo.es_autor_principal: 
                    tecnologia_rechazados += 1
            elif autor_trabajo.trabajo.subareas.first().area.id == 4:
                if not autor_trabajo.autor.id in autores_ciencias_sociales:
                    autores_ciencias_sociales.append(autor_trabajo.autor.id)

                if autor_trabajo.trabajo.estatus == "Aceptado" and autor_trabajo.es_autor_principal:
                    ciencias_sociales_aceptados += 1
                elif autor_trabajo.trabajo.estatus == "Rechazado" and autor_trabajo.es_autor_principal:
                    ciencias_sociales_rechazados += 1
            elif autor_trabajo.trabajo.subareas.first().area.id == 5:
                if not autor_trabajo.autor.id in autores_sociedad_fisica:
                    autores_sociedad_fisica.append(autor_trabajo.autor.id)

                if autor_trabajo.trabajo.estatus == "Aceptado" and autor_trabajo.es_autor_principal:
                    sociedad_fisica_aceptados += 1
                elif autor_trabajo.trabajo.estatus == "Rechazado" and autor_trabajo.es_autor_principal:
                    sociedad_fisica_rechazados += 1

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


        #El siguiente codigo es para contabilizar los autores por area que listamos
        autores_biociencias = len(autores_biociencias)
        autores_ciencias_exactas = len(autores_ciencias_exactas)
        autores_ciencias_sociales = len(autores_ciencias_sociales)
        autores_sociedad_fisica = len(autores_sociedad_fisica)
        autores_tecnologia = len(autores_tecnologia)

        data = {
            "trabajos": {
                "labels": ["Trabajos Aceptados", "Trabajos Rechazados", "Trabajos Pendientes"],
                "data": [trabajos_aceptados, trabajos_rechazados, trabajos_pendientes]
            },
            "arbitros": {
                "labels": ['Total arbitros', 'Invitaciones aceptadas', 'Invitaciones pendientes'],
                "data": [total_arbitros, invitaciones_aceptadas, invitaciones_pendientes]
            },
            "autores": {
                "labels": ['Educación Básica Primaria', 'Educación Básica Secundaria', 'Bachillerato/Educación Media', 'Educación Técnico/Profesional', 'Universidad', 'Postgrado'],
                "data": [educacion_primaria, educacion_secundaria, bachillerato, tecnico, universidad, postgrado]
            },
            "area":{
                "labels": ['Biociencias', 'Ciencias Exactas', 'Tecnología', 'Ciencias Sociales', 'CSVF'],
                "data_aceptados": [biociencias_aceptados, ciencias_exactas_aceptados, tecnologia_aceptados, ciencias_sociales_aceptados, sociedad_fisica_aceptados],
                "data_rechazados": [biociencias_rechazados, ciencias_exactas_rechazados, tecnologia_rechazados, ciencias_sociales_rechazados, sociedad_fisica_rechazados]
            },
            "autoresArea":{
                "labels": ['Biociencias', 'Ciencias Exactas', 'Tecnología', 'Ciencias Sociales', 'CSVF'],
                "data": [autores_biociencias, autores_ciencias_exactas, autores_tecnologia, autores_ciencias_sociales, autores_sociedad_fisica],
            },
        }   
        return Response(data)


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

