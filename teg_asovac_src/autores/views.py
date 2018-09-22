# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,redirect, get_object_or_404

from .models import Autor, Autores_trabajos, Pagador, Factura, Datos_pagador, Pago
from main_app.models import Rol,Sistema_asovac,Usuario_asovac
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status

from .forms import DatosPagadorForm, PagoForm, FacturaForm, EditarDatosPagadorForm, EditarPagoForm, EditarFacturaForm

from django.contrib import messages
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

	rol_id=get_roles(request.user.id)

	# print (rol_id)

	estado = request.session['estado']
	arbitraje_id = request.session['arbitraje_id']

	item_active = 2
	items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

	route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

	# print items

	context = {
		'nombre_vista' : 'Autores',
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
	return render(request, 'main_app_authors_list.html', context)

def author_edit(request):
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	arbitraje_id = request.session['arbitraje_id']
	
	item_active = 2
	items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

	route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

	# print items

	context = {
		'nombre_vista' : 'Editar autores',
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
	return render(request, 'main_app_author_edit.html', context)


#Vista para generar certificado
def generar_certificado(request):
	context={
		"nombre_vista": 'Generar Certificado'
	}
	return render(request,"autores_generar_certificado.html", context)


#Vista donde el autor ve los pagadores de sus trabajos y tiene opción de añadir nuevos
def postular_trabajo(request):
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	if request.POST:
		request.session['autor_trabajo_id'] = request.POST['autor_trabajo_id']
		return redirect('autores:postular_trabajo_pagador')
	else:
		rol_id=get_roles(request.user.id)

		# print (rol_id)
		estado = request.session['estado']
		event_id = request.session['arbitraje_id']
		
		item_active = 0
		items = validate_rol_status(estado,rol_id,item_active,event_id)

		route_conf = get_route_configuracion(estado,rol_id,event_id)
		route_seg = get_route_seguimiento(estado,rol_id)
		route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
		route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
		route_resultados = get_route_resultados(estado,rol_id, event_id)

		# print items


		#Lista de trabajos del autor
		usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
		autor = Autor.objects.get(usuario = usuario_asovac)
		sistema_asovac = Sistema_asovac.objects.get(id = event_id)
		autores_trabajos_list = Autores_trabajos.objects.filter(autor = autor, sistema_asovac = sistema_asovac)

		pagador_list = Pagador.objects.all()
		factura_list = Factura.objects.all()


	context = {
		"nombre_vista": 'Postular Trabajo',
	#	"pagadorform": pagadorform,
	#	"pagoform": pagoform,
	#	"facturaform": facturaform,
		'main_navbar_options' : main_navbar_options,
		'estado' : estado,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'autores_trabajos_list':autores_trabajos_list,
        'pagador_list': pagador_list,
        'factura_list':factura_list,
    }
	return render(request,"autores_postular_trabajo.html",context)


# Vista donde el autor introduce los datos del pagador
def postular_trabajo_pagador(request):
	
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	item_active = 0
	items =validate_rol_status(estado,rol_id,item_active, event_id)

	route_conf = get_route_configuracion(estado,rol_id, event_id)
	route_seg = get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, event_id)


	# print items
	autor_trabajo = get_object_or_404(Autores_trabajos, id = request.session['autor_trabajo_id'])
	pagadorform = DatosPagadorForm()

	request.session['pagador_forms'] = 0

	if request.method == "POST":
		pagadorform = DatosPagadorForm(request.POST)
		if pagadorform.is_valid():
			request.session['datos_pagador'] = pagadorform.cleaned_data
			request.session['pagador_forms'] = 1
			return redirect('autores:postular_trabajo_factura') 

	context = {
		"nombre_vista": 'Postular Trabajo - Pago',
		"pagadorform": pagadorform,
		'main_navbar_options' : main_navbar_options,
		'estado' : estado,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'autor_trabajo':autor_trabajo,
    }

	return render(request,"autores_postular_trabajo_pagador.html",context)


#Vista donde el autor introduce los datos del pago
def postular_trabajo_pago(request):
	
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active, event_id)

	route_conf= get_route_configuracion(estado,rol_id, event_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, event_id)

	# print items
	print(request.session['factura']['fecha_emision'])
	pagoform = PagoForm()
	autor_trabajo = get_object_or_404(Autores_trabajos, id = request.session['autor_trabajo_id'])
	if request.method == "POST":
		pagoform = PagoForm(request.POST, request.FILES)
		if pagoform.is_valid():
			datos_pagador = Datos_pagador(cedula = request.session['datos_pagador']['cedula'], nombres = request.session['datos_pagador']['nombres'], apellidos = request.session['datos_pagador']['apellidos'], pasaporte_rif = request.session['datos_pagador']['pasaporte_rif'], telefono_oficina = request.session['datos_pagador']['telefono_oficina'], telefono_habitacion_celular = request.session['datos_pagador']['telefono_habitacion_celular'], direccion_fiscal = request.session['datos_pagador']['direccion_fiscal'])
			datos_pagador.save()
			pagador = Pagador(autor_trabajo = autor_trabajo, datos_pagador = datos_pagador)
			pagador.save()
			pago = pagoform.save()
			factura = Factura(pagador = pagador, pago = pago, monto_subtotal = request.session['factura']['monto_subtotal'], iva = request.session['factura']['iva'], monto_total = request.session['factura']['monto_total'], fecha_emision = request.session['factura']['fecha_emision'])
			factura.save()
			autor_trabajo.monto_total = autor_trabajo.monto_total - factura.monto_total
			autor_trabajo.save()
			request.session['pagador_forms'] = 1
			return redirect('autores:postular_trabajo')
	context = {
		"nombre_vista": 'Postular Trabajo - Pago',
		"pagoform": pagoform,
		'main_navbar_options' : main_navbar_options,
		'estado' : estado,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'autor_trabajo': autor_trabajo,
    }
	if request.session['pagador_forms'] != 2:
		return redirect('autores:postular_trabajo_pagador')

	return render(request,"autores_postular_trabajo_pago.html",context)


#Vista donde el autor introduce datos de la factura
def postular_trabajo_factura(request):
	


	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active, event_id)

	route_conf= get_route_configuracion(estado,rol_id, event_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, event_id)

	# print items
	autor_trabajo = get_object_or_404(Autores_trabajos, id = request.session['autor_trabajo_id'])

	facturaform = FacturaForm()
	if request.method == "POST":
		facturaform = FacturaForm(request.POST)
		if facturaform.is_valid():
			#request.session['factura_monto_subtotal'] = facturaform.cleaned_data['monto_subtotal']
			#request.session['factura_iva'] = facturaform.cleaned_data['iva']
			#request.session['factura_monto_total'] = facturaform.cleaned_data['monto_total']
			factura = {
				'monto_subtotal': facturaform.cleaned_data['monto_subtotal'],
				'iva': facturaform.cleaned_data['iva'],
				'monto_total': facturaform.cleaned_data['monto_total'],
				'fecha_emision': str(facturaform.cleaned_data['fecha_emision']), }
			request.session['factura'] = factura
			request.session['pagador_forms'] = 2
			return redirect('autores:postular_trabajo_pago') 


	context = {
		"nombre_vista": 'Postular Trabajo - Factura',
		"facturaform": facturaform,
		'main_navbar_options' : main_navbar_options,
		'estado' : estado,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'autor_trabajo':autor_trabajo,
    }

	if(request.session['pagador_forms'] != 1):
		return redirect('autores:postular_trabajo_pagador')

	return render(request,"autores_postular_trabajo_factura.html",context)


#Detalles del pago
def detalles_pago(request, pagador_id):

	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active, event_id)

	route_conf= get_route_configuracion(estado,rol_id, event_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, event_id)

	# print items
	usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
	autor = Autor.objects.get(usuario = usuario_asovac)
	sistema_asovac = Sistema_asovac.objects.get(id = event_id)

	pagador = get_object_or_404(Pagador, id = pagador_id)
	factura = get_object_or_404(Factura, pagador = pagador)
	autor_trabajo = get_object_or_404(Autores_trabajos ,autor = autor, sistema_asovac = sistema_asovac, trabajo = pagador.autor_trabajo.trabajo)
	

	

	context = {
		"nombre_vista": 'Postular Trabajo - Detalles del pago',
		'main_navbar_options' : main_navbar_options,
		'estado' : estado,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'pagador': pagador,
        'autor_trabajo': autor_trabajo,
        'factura': factura,
    }

	return render(request,"autores_detalles_pago.html",context)


#Editar datos del pagador
def editar_datos_pagador(request, pagador_id):
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active, event_id)

	route_conf= get_route_configuracion(estado,rol_id, event_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, event_id)

	# print items
	usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
	autor = Autor.objects.get(usuario = usuario_asovac)
	sistema_asovac = Sistema_asovac.objects.get(id = event_id)

	pagador = get_object_or_404(Pagador, id = pagador_id)
	autor_trabajo = get_object_or_404(Autores_trabajos ,autor = autor, sistema_asovac = sistema_asovac, trabajo = pagador.autor_trabajo.trabajo)

	if request.method == "POST":
		if form.is_valid():
			form = EditarDatosPagadorForm(request.POST, instance = pagador.datos_pagador)
			form.save()
			messages.success(request, 'Sus cambios en los datos del pagador han sido guardados con éxito.')
			return redirect('autores:postular_trabajo')
	else:
		form = EditarDatosPagadorForm(instance = pagador.datos_pagador)
	

	context = {
		"nombre_vista": 'Postular Trabajo - Editar datos del pagador',
		'main_navbar_options' : main_navbar_options,
		'estado' : estado,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'pagador': pagador,
        'autor_trabajo': autor_trabajo,
        'pagadorform': form,
    }

	return render(request,"autores_editar_pagador.html",context)


#Editar datos del pago
def editar_pago(request, pago_id):
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active, event_id)

	route_conf= get_route_configuracion(estado,rol_id, event_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, event_id)

	# print items
	usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
	autor = Autor.objects.get(usuario = usuario_asovac)
	sistema_asovac = Sistema_asovac.objects.get(id = event_id)

	pago = get_object_or_404(Pago, id = pago_id)
	factura = get_object_or_404(Factura, pago = pago)
	autor_trabajo = get_object_or_404(Autores_trabajos ,autor = autor, sistema_asovac = sistema_asovac, trabajo = factura.pagador.autor_trabajo.trabajo)

	if request.method == "POST":
		if form.is_valid():
			form = EditarPagoForm(request.POST, instance = pago)
			form.save()
			messages.success(request, 'Sus cambios en los datos del pago han sido guardados con éxito.')
			return redirect('autores:postular_trabajo')
	else:
		form = EditarPagoForm(instance = pago)
	

	context = {
		"nombre_vista": 'Postular Trabajo - Editar datos del pagador',
		'main_navbar_options' : main_navbar_options,
		'estado' : estado,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'autor_trabajo': autor_trabajo,
        'pagoform': form,
    }

	return render(request,"autores_editar_pago.html",context)


#Editar datos del pago
def editar_factura(request, factura_id):
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	rol_id=get_roles(request.user.id)

	# print (rol_id)
	estado = request.session['estado']
	event_id = request.session['arbitraje_id']
	
	item_active = 0
	items=validate_rol_status(estado,rol_id,item_active, event_id)

	route_conf= get_route_configuracion(estado,rol_id, event_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, event_id)

	# print items
	usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
	autor = Autor.objects.get(usuario = usuario_asovac)
	sistema_asovac = Sistema_asovac.objects.get(id = event_id)

	factura = get_object_or_404(Factura, id = factura_id)
	autor_trabajo = get_object_or_404(Autores_trabajos ,autor = autor, sistema_asovac = sistema_asovac, trabajo = factura.pagador.autor_trabajo.trabajo)
	monto_anterior= factura.monto_total
	if request.method == "POST":
		form = EditarFacturaForm(request.POST, instance = factura)
		if form.is_valid():
			monto_nuevo = autor_trabajo.monto_total -  (form.cleaned_data['monto_total']  - monto_anterior) 
			form.save()
			autor_trabajo.monto_total = monto_nuevo
			autor_trabajo.save()
			messages.success(request, 'Sus cambios en los datos de la factura han sido guardados con éxito.')
			return redirect('autores:postular_trabajo')
	else:
		form = EditarFacturaForm(instance = factura)
	

	context = {
		"nombre_vista": 'Postular Trabajo - Editar datos del pagador',
		'main_navbar_options' : main_navbar_options,
		'estado' : estado,
		'rol_id' : rol_id,
		'event_id' : event_id,
		'item_active' : item_active,
		'items':items,
		'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'autor_trabajo': autor_trabajo,
        'facturaform': form,
    }

	return render(request,"autores_editar_factura.html",context)
