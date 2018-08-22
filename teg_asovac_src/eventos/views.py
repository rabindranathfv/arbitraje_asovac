# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from main_app.models import Rol,Sistema_asovac,Usuario_asovac

from main_app.views import get_route_resultados, get_route_trabajos_navbar, verify_trabajo_options, get_route_trabajos_sidebar, verify_asignar_sesion, get_roles, verify_configuration, verify_arbitration,verify_result,verify_event,validate_rol_status,verify_configuracion_general_option,verify_datos_basicos_option,verify_estado_arbitrajes_option,verify_usuario_option,verify_asignacion_coordinador_general_option,verify_asignacion_coordinador_area_option,verify_recursos_option,verify_areas_subareas_option,verify_autores_option,verify_arbitros_option,verify_sesions_arbitraje_option,verify_arbitraje_option,verify_trabajo_option,verify_eventos_sidebar_full,verify_espacio_option,validate_rol_status,get_route_configuracion,get_route_seguimiento, verify_jobs
from eventos.forms import CreateOrganizerForm,CreateEventForm
from eventos.models import Organizador,Organizador_evento,Evento,Locacion_evento

from main_app.models import Usuario_asovac,Sistema_asovac,Rol

# Create your views here.
def event_list(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Eventos',  'icon': 'fa-archive',   'active': True}]

    secondary_navbar_options = ['']

    # rol_id = get_roles(request.user.id)


    #print (rol_id)
    # estado = request.session['estado']
    # arbitraje_id = request.session['arbitraje_id']


    # item_active = 4
    # items=validate_rol_status(estado,rol_id,item_active)


    # route_conf= get_route_configuracion(estado,rol_id)
    # route_seg= get_route_seguimiento(estado,rol_id)
    # route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    # route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    # route_resultados = get_route_resultados(estado,rol_id)
    # print items


    context = {
        'nombre_vista' : 'Eventos',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        # 'estado' : estado,
        # #'rol' : rol,
        # 'rol_id' : rol_id,
        # 'arbitraje_id' : arbitraje_id,
        # 'item_active' : item_active,
        # 'items':items,
        # 'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        # 'usuarios_sidebar' : items["usuarios_sidebar"][0],
        # 'recursos_sidebar' : items["recursos_sidebar"][0],
        # 'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        # 'autores_sidebar' : items["autores_sidebar"][0],
        # 'arbitros_sidebar' : items["arbitros_sidebar"][0],
        # 'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        # 'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        # 'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        # 'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        # 'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        # 'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        # 'trabajos_sidebar':items["trabajos_sidebar"][0],
        # 'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        # 'espacio_sidebar':items["espacio_sidebar"][0],
        # 'asignacion_de_sesion_sidebar':items["asignacion_de_sesion_sidebar"][0],
        # 'trabajo_sidebar': items["trabajo_sidebar"][0],
        # 'verify_configuration':items["configuration"][0],
        # 'verify_arbitration':items["arbitration"][0],
        # 'verify_result':items["result"][0],
        # 'verify_event':items["event"][0],
        # 'verify_jobs':items["jobs"][0],
        # 'route_conf':route_conf,
        # 'route_seg':route_seg,
        # 'route_trabajos_sidebar':route_trabajos_sidebar,
        # 'route_trabajos_navbar': route_trabajos_navbar,
        # 'route_resultados': route_resultados,
    }
    return render(request, 'eventos_event_list.html', context)


def event_edit(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Eventos',  'icon': 'fa-archive',   'active': True}]

    secondary_navbar_options = ['']

    rol_id=get_roles(request.user.id)

    # print (rol_id)
    # estado = request.session['estado']
    # arbitraje_id = request.session['arbitraje_id']

    # # print (rol_id)
    # estado = request.session['estado']
    # event_id = request.session['arbitraje_id']


    # route_conf = get_route_configuracion(estado,rol_id)
    # route_seg = get_route_seguimiento(estado,rol_id)
    # route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    # route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    # route_resultados = get_route_resultados(estado,rol_id)
    # print items

    # item_active = 4
    # items=validate_rol_status(estado,rol_id,item_active)

    context = {
        'nombre_vista' : 'Autores',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        # 'estado' : estado,
        # #'rol' : rol,
        # 'rol_id' : rol_id,
        # 'arbitraje_id' : arbitraje_id,
        # 'item_active' : item_active,
        # 'items':items,
        # 'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        # 'usuarios_sidebar' : items["usuarios_sidebar"][0],
        # 'recursos_sidebar' : items["recursos_sidebar"][0],
        # 'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        # 'autores_sidebar' : items["autores_sidebar"][0],
        # 'arbitros_sidebar' : items["arbitros_sidebar"][0],
        # 'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        # 'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        # 'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        # 'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        # 'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        # 'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        # 'trabajos_sidebar':items["trabajos_sidebar"][0],
        # 'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        # 'espacio_sidebar':items["espacio_sidebar"][0],
        # 'asignacion_de_sesion_sidebar':items["asignacion_de_sesion_sidebar"][0],
        # 'trabajo_sidebar': items["trabajo_sidebar"][0],
        # 'verify_configuration':items["configuration"][0],
        # 'verify_arbitration':items["arbitration"][0],
        # 'verify_result':items["result"][0],
        # 'verify_event':items["event"][0],
        # 'verify_jobs':items["jobs"][0],
        # 'route_conf':route_conf,
        # 'route_seg':route_seg,
        # 'route_trabajos_sidebar':route_trabajos_sidebar,
        # 'route_trabajos_navbar': route_trabajos_navbar,
        # 'route_resultados': route_resultados,
    }
    return render(request, 'eventos_event_edit.html', context)

def event_create(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Eventos',  'icon': 'fa-archive',   'active': True}]

    secondary_navbar_options = ['']

    form = CreateEventForm()
    context = {
        'username' : request.user.username,
        'form' : form,
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
    }
    if request.method == 'POST':
        form = CreateOrganizerForm(request.POST or None)
        if form.is_valid():
            form.save()
            print(form)
            organizer_data = Organizador.objects.all()
            context = {        
                'username' : request.user.username,
                'form' : form,
                'org_data': organizer_data,
                'main_navbar_options' : main_navbar_options,
                'secondary_navbar_options' : secondary_navbar_options,
                #'verify_event_app' : verify_event_app(),
                }
            return render(request, 'eventos_event_create.html', context) 

    #rol_id=get_roles(request.user.id)

    # print (rol_id)
    # estado = request.session['estado']
    # arbitraje_id = request.session['arbitraje_id']

    
    # item_active = 4
    # items=validate_rol_status(estado,rol_id,item_active)

    # route_conf= get_route_configuracion(estado,rol_id)
    # route_seg= get_route_seguimiento(estado,rol_id)
    # route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    # route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    # route_resultados = get_route_resultados(estado,rol_id)
    # print items


    #context = {
        #'nombre_vista' : 'Eventos',
        #'main_navbar_options' : main_navbar_options,
        #'secondary_navbar_options' : secondary_navbar_options,
        # 'estado' : estado,
        # #'rol' : rol,
        # 'rol_id' : rol_id,
        # 'arbitraje_id' : arbitraje_id,
        # 'item_active' : item_active,
        # 'items':items,
        # 'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        # 'usuarios_sidebar' : items["usuarios_sidebar"][0],
        # 'recursos_sidebar' : items["recursos_sidebar"][0],
        # 'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        # 'autores_sidebar' : items["autores_sidebar"][0],
        # 'arbitros_sidebar' : items["arbitros_sidebar"][0],
        # 'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        # 'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        # 'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        # 'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        # 'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        # 'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        # 'trabajos_sidebar':items["trabajos_sidebar"][0],
        # 'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        # 'espacio_sidebar':items["espacio_sidebar"][0],
        # 'asignacion_de_sesion_sidebar':items["asignacion_de_sesion_sidebar"][0],
        # 'trabajo_sidebar': items["trabajo_sidebar"][0],
        # 'verify_configuration':items["configuration"][0],
        # 'verify_arbitration':items["arbitration"][0],
        # 'verify_result':items["result"][0],
        # 'verify_event':items["event"][0],
        # 'verify_jobs':items["jobs"][0],
        # 'route_conf':route_conf,
        # 'route_seg':route_seg,
        # 'route_trabajos_sidebar':route_trabajos_sidebar,
        # 'route_trabajos_navbar': route_trabajos_navbar,
        # 'route_resultados': route_resultados,
    #}
    return render(request, 'eventos_event_create.html', context)

def organizer_create(request):
    form = CreateOrganizerForm()
    print(request.user.id)
    #print(request.user.username)
    user_data = Usuario_asovac.objects.get(pk=request.user.id)
    print(user_data.Sistema_asovac_id.values())
    #user_asov.save()
    # arbitraje al cual pertenece el usuario
    #arbitraje = Sistema_asovac.objects.filter().only(id)
    #print(arbitraje)

    context = {
        'username' : request.user.username,
        'form' : form,
    }
    if request.method == 'POST':
        form = CreateOrganizerForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False)

            print(form)
            organizer_data = Organizador.objects.all()
            context = {        
                'username' : request.user.username,
                'form' : form,
                'org_data': organizer_data,
                'verify_event_app' : verify_event_app(),
                }
            return render(request, 'eventos_organizer_list.html', context) 
    return render(request, 'eventos_organizer_create.html',context)

def organizer_list(request):

    return render(request, 'eventos_organizer_list.html', context={})

def organizer_edit(request):

    return render(request, 'eventos_organizer_edit.html', context={})

def organizer_delete(request):

    return render(request, 'eventos_organizer_delete.html',context={})

def organizer_detail(request):
    
    return render(request, 'eventos_organizer_detail.html',context={})