# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from .forms import TrabajoForm
from main_app.models import Rol,Sistema_asovac,Usuario_asovac
from main_app.views import get_roles, verify_configuration, verify_arbitration,verify_result,verify_event,validate_rol_status,verify_configuracion_general_option,verify_datos_basicos_option,verify_estado_arbitrajes_option,verify_usuario_option,verify_asignacion_coordinador_general_option,verify_asignacion_coordinador_area_option,verify_recursos_option,verify_areas_subareas_option,verify_autores_option,verify_arbitros_option,verify_sesions_arbitraje_option,verify_arbitraje_option,verify_trabajo_option,verify_eventos_sidebar_full,verify_espacio_option,validate_rol_status,get_route_configuracion,get_route_seguimiento

#Vista donde están la lista de trabajos del autor y dónde se le permite crear, editar o eliminar trabajos
def trabajos(request):
    form = TrabajoForm()
    context = {
        "nombre_vista": 'Autores',
        "form": form,
    }
    return render(request,"trabajos.html",context)

def jobs_list(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = [' ']

    rol_id=get_roles(request.user.id)


    estado = request.session['estado']
    event_id = request.session['arbitraje_id']

    #item_active = 2
    if request.session['item_active'] != 2:
        request.session['item_active'] = 2
        item_active = request.session['item_active']
        validate_rol_status(estado,rol_id,item_active,request)

    #route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    #route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))

    # print items

    context = {
        'nombre_vista' : 'Trabajos',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        #'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        #'item_active' : item_active,
        #'items':items,
        'configuracion_general_sidebar': request.session['configuracion_general_sidebar'],
        'usuarios_sidebar' : request.session['usuarios_sidebar'],
        'recursos_sidebar' : request.session['recursos_sidebar'],
        'areas_subareas_sidebar' : request.session['areas_subareas_sidebar'],
        'autores_sidebar' : request.session['autores_sidebar'],
        'arbitros_sidebar' : request.session['arbitros_sidebar'],
        'sesion_arbitraje_sidebar' : request.session['sesion_arbitraje_sidebar'],
        'arbitraje_sidebar' : request.session['arbitraje_sidebar'],
        'eventos_sidebar_full' : request.session['eventos_sidebar_full'],
        'asignacion_coordinador_general': request.session['asignacion_coordinador_general'],
        'asignacion_coordinador_area': request.session['asignacion_coordinador_area'],
        'datos_basicos_sidebar' : request.session['datos_basicos_sidebar'],
        'trabajos_sidebar':request.session['trabajos_sidebar'],
        'estado_arbitrajes_sidebar':request.session['estado_arbitrajes_sidebar'],
        'espacio_sidebar':request.session['espacio_sidebar'],
        'verify_configuration':request.session['configuration'],
        'verify_arbitration':request.session['arbitration'],
        'verify_result':request.session['result'],
        'verify_event':request.session['event'],
        #'route_conf':route_conf,
        #'route_seg':route_seg,
    }
    return render(request, 'trabajos_jobs_list.html', context)

def jobs_edit(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = [' ']

    rol_id=get_roles(request.user.id)

    estado = request.session['estado']
    event_id = request.session['arbitraje_id']

    #item_active = 2
    if request.session['item_active'] != 2:
        request.session['item_active'] = 2
        item_active = request.session['item_active']
        validate_rol_status(estado,rol_id,item_active,request)

    #route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    #route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))

    # print items

    context = {
        'nombre_vista' : 'Trabajos',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        #'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        #'item_active' : item_active,
        #'items':items,
        'configuracion_general_sidebar': request.session['configuracion_general_sidebar'],
        'usuarios_sidebar' : request.session['usuarios_sidebar'],
        'recursos_sidebar' : request.session['recursos_sidebar'],
        'areas_subareas_sidebar' : request.session['areas_subareas_sidebar'],
        'autores_sidebar' : request.session['autores_sidebar'],
        'arbitros_sidebar' : request.session['arbitros_sidebar'],
        'sesion_arbitraje_sidebar' : request.session['sesion_arbitraje_sidebar'],
        'arbitraje_sidebar' : request.session['arbitraje_sidebar'],
        'eventos_sidebar_full' : request.session['eventos_sidebar_full'],
        'asignacion_coordinador_general': request.session['asignacion_coordinador_general'],
        'asignacion_coordinador_area': request.session['asignacion_coordinador_area'],
        'datos_basicos_sidebar' : request.session['datos_basicos_sidebar'],
        'trabajos_sidebar':request.session['trabajos_sidebar'],
        'estado_arbitrajes_sidebar':request.session['estado_arbitrajes_sidebar'],
        'espacio_sidebar':request.session['espacio_sidebar'],
        'verify_configuration':request.session['configuration'],
        'verify_arbitration':request.session['arbitration'],
        'verify_result':request.session['result'],
        'verify_event':request.session['event'],
        #'route_conf':route_conf,
        #'route_seg':route_seg,
    }
    return render(request, 'trabajos_jobs_edit.html', context)
   

# Vista para editar trabajos
def edit_trabajo(request):
	form = TrabajoForm()
	context = {
		"nombre_vista": 'Editar Trabajo',
		"form": form,
    }
	return render(request,"trabajos_edit_trabajo.html",context)

#Vista donde aparecen los trabajos evaluados
def trabajos_evaluados(request):
	context = {
		"nombre_vista": 'Trabajos Evaluados'
	}
	return render(request,"trabajos_trabajos_evaluados.html",context)

