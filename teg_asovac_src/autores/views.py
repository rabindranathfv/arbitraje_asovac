# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from .models import Autor, Autores_trabajos, Pagador, Factura, Datos_pagador, Pago
from main_app.models import Rol,Sistema_asovac,Usuario_asovac, User
from trabajos.models import Detalle_version_final
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status
from trabajos.views import show_areas_modal

from .forms import DatosPagadorForm, PagoForm, FacturaForm, AdminCreateAutorForm

from django.contrib import messages

from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
# Create your views here.
def admin_create_author(request):
	if request.method == "POST":
		form = AdminCreateAutorForm(request.POST)
		if form.is_valid():
			new_autor = form.save(commit = False)
			usuario = User.objects.get(email = new_autor.correo_electronico)
			usuario_asovac = Usuario_asovac.objects.get(usuario = usuario)
			new_autor.usuario = usuario_asovac
			new_autor.save()
			return redirect('autores:authors_list')
	else:
		main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
	                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
	                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
	                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

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
		form = AdminCreateAutorForm()
		context = {
			"nombre_vista": 'Administración - Crear Autor',
			'main_navbar_options' : main_navbar_options,
			'estado' : estado,
			'rol_id' : rol_id,
			'event_id' : event_id,
			'arbitraje_id' : event_id,
			'item_active' : item_active,
			'items':items,
			'route_conf':route_conf,
	        'route_seg':route_seg,
	        'route_trabajos_sidebar':route_trabajos_sidebar,
	        'route_trabajos_navbar': route_trabajos_navbar,
	        'route_resultados': route_resultados,
	        'form': form,
	    }
	return render(request,"autores_admin_create_author.html",context)


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

	# request.session para almacenar el item seleccionado del sidebar
	request.session['sidebar_item'] = "Autores"

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
	return render(request, 'autores_authors_list.html', context)


def list_authors (request):
    response = {}
    response['query'] = []

    sort= request.POST['sort']
    search= request.POST['search']
    # Se verifica la existencia del parametro
    if request.POST.get('offset', False) != False:
        init= int(request.POST['offset'])
    
    # Se verifica la existencia del parametro
    if request.POST.get('limit', False) != False:
        limit= int(request.POST['limit'])+init
    
    # init= int(request.POST['offset'])
    # limit= int(request.POST['limit'])+init
    # print "init: ",init,"limit: ",limit

    if request.POST['order'] == 'asc':
        if sort == 'fields.nombres':
            order='nombres'
        else:
            if sort == 'fields.apellidos':
                order='apellidos'
            else:
                order=sort
    else:
        if sort == 'fields.nombres':
            order='-nombres'
        else:
            if sort == 'fields.apellidos':
                order='-apellidos'
            else:
                order='-'+sort

    if search != "":
        data=Autor.objects.all().filter( Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cedula_pasaporte__icontains=search) | Q(correo_electronico__icontains=search) | Q(universidad__nombre__icontains=search)).order_by(order)#[:limit]
        total= len(data)
    else:
        if request.POST.get('limit', False) == False or request.POST.get('offset', False) == False:
            print "consulta para exportar"
            print Autor.objects.all().order_by(order).query
            data=Autor.objects.all().order_by(order)
            total= Autor.objects.all().count()
        else:
            print "consulta normal"
            # print Area.objects.all().order_by(order)[init:limit].query
            test= Autor.objects.all().order_by(order)[init:limit]
            data=Autor.objects.all().order_by(order)[init:limit]
            total= Autor.objects.all().count()
            # test=Area.objects.raw('SELECT a.*, (SELECT count(area.id) FROM main_app_area as area) FROM main_app_area as a LIMIT %s OFFSET %s',[limit,init])
    # response['total']=total
    # print response
    for item in data:
        # print("%s is %s. and total is %s" % (item.nombre, item.descripcion,item.count))
        response['query'].append({'id':item.id, 'nombres':item.nombres,'apellidos': item.apellidos,'correo_electronico': item.correo_electronico, 'cedula_pasaporte': item.cedula_pasaporte,'universidad': item.universidad.nombre })

    response={
        'total': total,
        'query': response,
    }
   
    return JsonResponse(response)



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
		'arbitraje_id' : event_id,
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


#Modal para crear datos del pagador
def postular_trabajo_pagador_modal(request, autor_trabajo_id):
	data = dict()
	autor_trabajo = get_object_or_404(Autores_trabajos, id = autor_trabajo_id)

	if request.method == "POST":
		form = DatosPagadorForm(request.POST)
		if form.is_valid():
			request.session['datos_pagador'] = form.cleaned_data
			data['url'] = reverse('autores:postular_trabajo_factura_modal', kwargs={'autor_trabajo_id':autor_trabajo_id})
			data['message'] = "Formulario de pagador llenado con éxito, llene el siguiente formulario"
	else:
		form = DatosPagadorForm()
		context ={
			'form': form,
			'autor_trabajo': autor_trabajo,
		}
		data['html_form'] = render_to_string('ajax/postular_trabajo_datos_pagador.html', context, request=request)
	return JsonResponse(data)


#Modal para crear datos de la factura
def postular_trabajo_factura_modal(request, autor_trabajo_id):
	data = dict()
	autor_trabajo = get_object_or_404(Autores_trabajos, id = autor_trabajo_id)

	if request.method == "POST":
		form = FacturaForm(request.POST)
		if form.is_valid():
			factura = {
				'monto_subtotal': form.cleaned_data['monto_subtotal'],
				'iva': form.cleaned_data['iva'],
				'monto_total': form.cleaned_data['monto_total'],
				'fecha_emision': str(form.cleaned_data['fecha_emision']), }
			request.session['factura'] = factura
			data['url'] = reverse('autores:postular_trabajo_pago_modal', kwargs={'autor_trabajo_id':autor_trabajo_id})
			data['message'] = "Formulario de factura llenado con éxito, llene el siguiente formulario"

	else:
		form =	FacturaForm()
		context ={
			'form': form,
			'autor_trabajo': autor_trabajo,
		}
		data['html_form'] = render_to_string('ajax/postular_trabajo_datos_factura.html', context, request=request)
	return JsonResponse(data)


#Modal para crear datos de la factura
def postular_trabajo_pago_modal(request, autor_trabajo_id):
	data = dict()
	autor_trabajo = get_object_or_404(Autores_trabajos, id = autor_trabajo_id)

	if request.method == "POST":
		form = PagoForm(request.POST, request.FILES)
		if form.is_valid():
			print("LLegó Aquí")
			datos_pagador = Datos_pagador(cedula = request.session['datos_pagador']['cedula'], nombres = request.session['datos_pagador']['nombres'], apellidos = request.session['datos_pagador']['apellidos'], pasaporte_rif = request.session['datos_pagador']['pasaporte_rif'], telefono_oficina = request.session['datos_pagador']['telefono_oficina'], telefono_habitacion_celular = request.session['datos_pagador']['telefono_habitacion_celular'], direccion_fiscal = request.session['datos_pagador']['direccion_fiscal'])
			datos_pagador.save()
			pagador = Pagador(autor_trabajo = autor_trabajo, datos_pagador = datos_pagador)
			pagador.save()
			pago = form.save()
			factura = Factura(pagador = pagador, pago = pago, monto_subtotal = request.session['factura']['monto_subtotal'], iva = request.session['factura']['iva'], monto_total = request.session['factura']['monto_total'], fecha_emision = request.session['factura']['fecha_emision'])
			factura.save()
			autor_trabajo.monto_total = autor_trabajo.monto_total - factura.monto_total
			autor_trabajo.save()
			if autor_trabajo.monto_total <= 0:
				trabajo_version_final = Detalle_version_final(trabajo = autor_trabajo.trabajo)
				trabajo_version_final.save()

			print(request.session['factura']['monto_total'])
			print(request.session['datos_pagador']['nombres'])

			return redirect('autores:postular_trabajo')

	else:
		form =	PagoForm()
		context ={
			'form': form,
			'autor_trabajo': autor_trabajo,
		}
		data['html_form'] = render_to_string('ajax/postular_trabajo_datos_pago.html', context, request=request)
	return JsonResponse(data)



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
		'arbitraje_id' : event_id,
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
