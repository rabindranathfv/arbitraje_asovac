# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from .forms import DatosPagadorForm, PagoForm, FacturaForm
from main_app.models import Rol,Sistema_asovac,Usuario_asovac
from main_app.views import get_route_resultados, get_route_trabajos_navbar, verify_trabajo_options, get_route_trabajos_sidebar, verify_asignar_sesion, get_roles, verify_configuration, verify_arbitration,verify_result,verify_event,validate_rol_status,verify_configuracion_general_option,verify_datos_basicos_option,verify_estado_arbitrajes_option,verify_usuario_option,verify_asignacion_coordinador_general_option,verify_asignacion_coordinador_area_option,verify_recursos_option,verify_areas_subareas_option,verify_autores_option,verify_arbitros_option,verify_sesions_arbitraje_option,verify_arbitraje_option,verify_trabajo_option,verify_eventos_sidebar_full,verify_espacio_option,validate_rol_status,get_route_configuracion,get_route_seguimiento, verify_jobs

# Create your views here.
def autores_pag(request):
    context = {
        "nombre_vista": 'autores'
    }
    return render(request,"test_views.html",context)

def authors_list(request):
    
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
							{'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
							{'title':'Resultados',      'icon': 'fa-chart-area','active': False},
							{'title':'Administración',  'icon': 'fa-archive',   'active': False}]
	
	secondary_navbar_options = ['']

	rol_id=get_roles(request.user.id)

	# print (rol_id)

	estado = request.session['estado']
	event_id = request.session['arbitraje_id']

	item_active = 2
	items=validate_rol_status(estado,rol_id,item_active)

	route_conf= get_route_configuracion(estado,rol_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id)

	# print items

	context = {
		'nombre_vista' : 'Autores',
		'main_navbar_options' : main_navbar_options,
		'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		#'rol' : rol,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
		'usuarios_sidebar' : items["usuarios_sidebar"][0],
		'recursos_sidebar' : items["recursos_sidebar"][0],
		'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
		'autores_sidebar' : items["autores_sidebar"][0],
		'arbitros_sidebar' : items["arbitros_sidebar"][0],
		'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
		'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
		'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
		'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
		'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
		'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
		'trabajos_sidebar':items["trabajos_sidebar"][0],
		'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
		'espacio_sidebar':items["espacio_sidebar"][0],
		'asignacion_de_sesion_sidebar':items["asignacion_de_sesion_sidebar"][0],
		'trabajo_sidebar': items["trabajo_sidebar"][0],
		'verify_configuration':items["configuration"][0],
		'verify_arbitration':items["arbitration"][0],
		'verify_result':items["result"][0],
		'verify_event':items["event"][0],
		'verify_jobs':items["jobs"][0],
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
	return render(request, 'main_app_authors_list.html', context)

def author_edit(request):
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
	secondary_navbar_options = ['']

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 2
	items=validate_rol_status(estado,rol_id,item_active)

	route_conf= get_route_configuracion(estado,rol_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id)

	# print items

	context = {
		'nombre_vista' : 'Editar autores',
		'main_navbar_options' : main_navbar_options,
		'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		#'rol' : rol,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
		'usuarios_sidebar' : items["usuarios_sidebar"][0],
		'recursos_sidebar' : items["recursos_sidebar"][0],
		'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
		'autores_sidebar' : items["autores_sidebar"][0],
		'arbitros_sidebar' : items["arbitros_sidebar"][0],
		'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
		'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
		'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
		'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
		'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
		'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
		'trabajos_sidebar':items["trabajos_sidebar"][0],
		'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
		'espacio_sidebar':items["espacio_sidebar"][0],
		'asignacion_de_sesion_sidebar':items["asignacion_de_sesion_sidebar"][0],
		'trabajo_sidebar': items["trabajo_sidebar"][0],
		'verify_configuration':items["configuration"][0],
		'verify_arbitration':items["arbitration"][0],
		'verify_result':items["result"][0],
		'verify_event':items["event"][0],
		'verify_jobs':items["jobs"][0],
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
	return render(request, 'main_app_author_edit.html', context)


#Vista para generar certificado
def generar_certificado(request):
	context={
		"nombre_vista": 'Generar Certificado'
	}
	return render(request,"autores_generar_certificado.html", context)


#Vista donde el autor ve los pagadores de sus trabajos y tiene opción de añadir nuevos
def postular_trabajo(request):
	pagadorform = DatosPagadorForm()
	pagoform = PagoForm()
	facturaform = FacturaForm()
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
	secondary_navbar_options = ['']

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active)

	route_conf= get_route_configuracion(estado,rol_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id)

	# print items

	context = {
		"nombre_vista": 'Postular Trabajo',
		"pagadorform": pagadorform,
		"pagoform": pagoform,
		"facturaform": facturaform,
		'main_navbar_options' : main_navbar_options,
		'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		#'rol' : rol,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
		'usuarios_sidebar' : items["usuarios_sidebar"][0],
		'recursos_sidebar' : items["recursos_sidebar"][0],
		'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
		'autores_sidebar' : items["autores_sidebar"][0],
		'arbitros_sidebar' : items["arbitros_sidebar"][0],
		'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
		'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
		'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
		'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
		'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
		'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
		'trabajos_sidebar':items["trabajos_sidebar"][0],
		'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
		'espacio_sidebar':items["espacio_sidebar"][0],
		'asignacion_de_sesion_sidebar':items["asignacion_de_sesion_sidebar"][0],
		'trabajo_sidebar': items["trabajo_sidebar"][0],
		'verify_configuration':items["configuration"][0],
		'verify_arbitration':items["arbitration"][0],
		'verify_result':items["result"][0],
		'verify_event':items["event"][0],
		'verify_jobs':items["jobs"][0],
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
	return render(request,"autores_postular_trabajo.html",context)


# Vista donde el autor introduce los datos del pagador
def postular_trabajo_pagador(request):
	pagadorform = DatosPagadorForm()
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
	secondary_navbar_options = ['']

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active)

	route_conf= get_route_configuracion(estado,rol_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id)

	# print items

	context = {
		"nombre_vista": 'Postular Trabajo - Pago',
		"pagadorform": pagadorform,
		'main_navbar_options' : main_navbar_options,
		'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		#'rol' : rol,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
		'usuarios_sidebar' : items["usuarios_sidebar"][0],
		'recursos_sidebar' : items["recursos_sidebar"][0],
		'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
		'autores_sidebar' : items["autores_sidebar"][0],
		'arbitros_sidebar' : items["arbitros_sidebar"][0],
		'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
		'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
		'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
		'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
		'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
		'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
		'trabajos_sidebar':items["trabajos_sidebar"][0],
		'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
		'espacio_sidebar':items["espacio_sidebar"][0],
		'asignacion_de_sesion_sidebar':items["asignacion_de_sesion_sidebar"][0],
		'trabajo_sidebar': items["trabajo_sidebar"][0],
		'verify_configuration':items["configuration"][0],
		'verify_arbitration':items["arbitration"][0],
		'verify_result':items["result"][0],
		'verify_event':items["event"][0],
		'verify_jobs':items["jobs"][0],
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }

	return render(request,"autores_postular_trabajo_pagador.html",context)


#Vista donde el autor introduce los datos del pago
def postular_trabajo_pago(request):
	pagoform = PagoForm()
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
	secondary_navbar_options = ['']

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active)

	route_conf= get_route_configuracion(estado,rol_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id)

	# print items

	context = {
		"nombre_vista": 'Postular Trabajo - Pago',
		"pagoform": pagoform,
		'main_navbar_options' : main_navbar_options,
		'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		#'rol' : rol,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
		'usuarios_sidebar' : items["usuarios_sidebar"][0],
		'recursos_sidebar' : items["recursos_sidebar"][0],
		'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
		'autores_sidebar' : items["autores_sidebar"][0],
		'arbitros_sidebar' : items["arbitros_sidebar"][0],
		'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
		'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
		'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
		'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
		'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
		'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
		'trabajos_sidebar':items["trabajos_sidebar"][0],
		'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
		'espacio_sidebar':items["espacio_sidebar"][0],
		'asignacion_de_sesion_sidebar':items["asignacion_de_sesion_sidebar"][0],
		'trabajo_sidebar': items["trabajo_sidebar"][0],
		'verify_configuration':items["configuration"][0],
		'verify_arbitration':items["arbitration"][0],
		'verify_result':items["result"][0],
		'verify_event':items["event"][0],
		'verify_jobs':items["jobs"][0],
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }

	return render(request,"autores_postular_trabajo_pago.html",context)


#Vista donde el autor introduce datos de la factura
def postular_trabajo_factura(request):
	facturaform = FacturaForm()

	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
	secondary_navbar_options = ['']

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active)

	route_conf= get_route_configuracion(estado,rol_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id)

	# print items

	context = {
		"nombre_vista": 'Postular Trabajo - Factura',
		"facturaform": facturaform,
		'main_navbar_options' : main_navbar_options,
		'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		#'rol' : rol,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
		'usuarios_sidebar' : items["usuarios_sidebar"][0],
		'recursos_sidebar' : items["recursos_sidebar"][0],
		'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
		'autores_sidebar' : items["autores_sidebar"][0],
		'arbitros_sidebar' : items["arbitros_sidebar"][0],
		'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
		'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
		'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
		'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
		'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
		'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
		'trabajos_sidebar':items["trabajos_sidebar"][0],
		'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
		'espacio_sidebar':items["espacio_sidebar"][0],
		'asignacion_de_sesion_sidebar':items["asignacion_de_sesion_sidebar"][0],
		'trabajo_sidebar': items["trabajo_sidebar"][0],
		'verify_configuration':items["configuration"][0],
		'verify_arbitration':items["arbitration"][0],
		'verify_result':items["result"][0],
		'verify_event':items["event"][0],
		'verify_jobs':items["jobs"][0],
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
	return render(request,"autores_postular_trabajo_factura.html",context)

