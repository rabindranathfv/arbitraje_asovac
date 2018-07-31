# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from .forms import DatosPagadorForm, PagoForm, FacturaForm
from main_app.models import Rol,Sistema_asovac,Usuario_asovac

# Global functions
# Esta función verifica que se va a desplegar la opción de configuracion general en el sidebar, retorna 1 si se usará y 0 sino.
def verify_configuracion_general_option(estado,rol_id,item_active): 
	if (estado == '0' and 1 in rol_id and item_active == 1):
		return 1
	return 0

def verify_usuario_option(estado,rol_id,item_active):
	if (estado == '0' and 1 in rol_id and item_active == 1):
		return 1
	return 0

def verify_recursos_option(estado,rol_id,item_active):
	if (estado == '0' and 1 in rol_id and item_active == 1):
		return 1
	return 0

def verify_areas_subareas_option(estado,rol_id,item_active):
	if (estado == '0' and 1 in rol_id and item_active == 1):
		return 1
	return 0


def verify_autores_option(estado,rol_id,item_active):
    if (estado == '0' and 1 in rol_id and item_active == 2):
        return 1
    return 0

def verify_arbitros_option(estado,rol_id, item_active):
    if (estado == '0' and 1 in rol_id and item_active == 2):
        return 1
    return 0

def verify_sesions_arbitraje_option(estado,rol_id, item_active):
    if (estado == '0' and 1 in rol_id and item_active == 2):
        return 1
    return 0

def verify_arbitraje_option(estado,rol_id, item_active):
    if (estado == '0' and 1 in rol_id and item_active == 2):
        return 1
    return 0

def verify_eventos_sidebar_full(estado,rol_id,item_active):
    if (estado == '0' and 1 in rol_id and item_active == 4):
        return 1
    return 0


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

	if request.POST:
		estado= request.POST['estado']
		event_id= request.POST['event_id']
	else:
		estado=-1
		event_id=-1

	rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()

	rol_id=[]
	for item in rol:
		rol_id.append(item.id)

	print (rol_id)

	item_active = 2
	configuracion_general_sidebar = verify_configuracion_general_option(estado, rol_id, item_active)
	usuarios_sidebar = verify_usuario_option(estado,rol_id,item_active)
	recursos_sidebar = verify_recursos_option(estado,rol_id,item_active)
	areas_subareas_sidebar = verify_areas_subareas_option(estado,rol_id,item_active)

	autores_sidebar = verify_autores_option(estado,rol_id,item_active)
	arbitros_sidebar = verify_arbitros_option(estado,rol_id,item_active)
	sesion_arbitraje_sidebar = verify_sesions_arbitraje_option(estado,rol_id,item_active)
	arbitraje_sidebar = verify_arbitraje_option(estado,rol_id,item_active)
	eventos_sidebar_full = verify_eventos_sidebar_full(estado,rol_id,item_active)
	context = {
        'nombre_vista' : 'Autores',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		'rol' : rol,
		'rol_id' : rol_id,
		'event_id' : event_id,
        'item_active' : '2',
        'username' : 'Username',
        'configuracion_general_sidebar': configuracion_general_sidebar,
        'usuarios_sidebar' : usuarios_sidebar,
        'recursos_sidebar' : recursos_sidebar,
        'areas_subareas_sidebar' : areas_subareas_sidebar,
        'autores_sidebar' : autores_sidebar,
        'arbitros_sidebar' : arbitros_sidebar,
        'sesion_arbitraje_sidebar' : sesion_arbitraje_sidebar,
        'arbitraje_sidebar' : arbitraje_sidebar,
        'eventos_sidebar_full' : eventos_sidebar_full,
    }
	return render(request, 'main_app_authors_list.html', context)

def author_edit(request):
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
	secondary_navbar_options = ['']
	if request.POST:
		estado= request.POST['estado']
		event_id= request.POST['event_id']
	else:
		estado=-1
		event_id=-1

	rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()

	rol_id=[]
	for item in rol:
		rol_id.append(item.id)

	print (rol_id)
	item_active = 2
	configuracion_general_sidebar = verify_configuracion_general_option(estado, rol_id, item_active)
	usuarios_sidebar = verify_usuario_option(estado,rol_id,item_active)
	recursos_sidebar = verify_recursos_option(estado,rol_id,item_active)
	areas_subareas_sidebar = verify_areas_subareas_option(estado,rol_id,item_active)

	autores_sidebar = verify_autores_option(estado,rol_id,item_active)
	arbitros_sidebar = verify_arbitros_option(estado,rol_id,item_active)
	sesion_arbitraje_sidebar = verify_sesions_arbitraje_option(estado,rol_id,item_active)
	arbitraje_sidebar = verify_arbitraje_option(estado,rol_id,item_active)
	eventos_sidebar_full = verify_eventos_sidebar_full(estado,rol_id,item_active)
	context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		'rol' : rol,
		'rol_id' : rol_id,
		'event_id' : event_id,
        'item_active' : '2',
        'username' : 'Username',
        'configuracion_general_sidebar': configuracion_general_sidebar,
        'usuarios_sidebar' : usuarios_sidebar,
        'recursos_sidebar' : recursos_sidebar,
        'areas_subareas_sidebar' : areas_subareas_sidebar,
        'autores_sidebar' : autores_sidebar,
        'arbitros_sidebar' : arbitros_sidebar,
        'sesion_arbitraje_sidebar' : sesion_arbitraje_sidebar,
        'arbitraje_sidebar' : arbitraje_sidebar,
        'eventos_sidebar_full' : eventos_sidebar_full,
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
	context = {
		"nombre_vista": 'Postular Trabajo',
		"pagadorform": pagadorform,
		"pagoform": pagoform,
		"facturaform": facturaform,
	}
	return render(request,"autores_postular_trabajo.html",context)


# Vista donde el autor introduce los datos del pagador
def postular_trabajo_pagador(request):
	pagadorform = DatosPagadorForm()
	context = {
		"nombre_vista": 'Postular Trabajo - Pagador',
		"pagadorform": pagadorform,
	}
	return render(request,"autores_postular_trabajo_pagador.html",context)


#Vista donde el autor introduce los datos del pago
def postular_trabajo_pago(request):
	pagoform = PagoForm()
	context = {
		"nombre_vista": 'Postular Trabajo - Pago',
		"pagoform": pagoform,
	}
	return render(request,"autores_postular_trabajo_pago.html",context)


#Vista donde el autor introduce datos de la factura
def postular_trabajo_factura(request):
	facturaform = FacturaForm()
	context = {
		"nombre_vista": 'Postular Trabajo - Factura',
		"facturaform": facturaform,
	}
	return render(request,"autores_postular_trabajo_factura.html",context)

