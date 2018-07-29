# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from .forms import DatosPagadorForm, PagoForm, FacturaForm
from main_app.models import Rol,Sistema_asovac,Usuario_asovac
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

	context = {
        'nombre_vista' : 'Autores',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		'rol' : rol,
		'event_id' : event_id,
        'item_active' : '2',
        'username' : 'Username',
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

	context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
		'estado' : estado,
		'rol' : rol,
		'event_id' : event_id,
        'item_active' : '2',
        'username' : 'Username',
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

