# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random 

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.template.loader import get_template

from main_app.models import Rol,Sistema_asovac,Usuario_asovac
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status

from .utils import render_to_pdf

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from arbitrajes.models import Arbitraje
from autores.models import Autores_trabajos, Autor
from main_app.models import Usuario_rol_in_sistema, Area
from trabajos.models import Trabajo, Trabajo_arbitro

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
                "labels": ['Total arbitros', 'Invitaciones aceptadas', 'Invitaciones pendientes'],
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