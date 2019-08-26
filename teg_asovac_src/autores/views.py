# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random, string,xlrd,os,sys,xlwt
from openpyxl import Workbook
from decouple import config
from django.conf import settings
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from .models import Autor, Autores_trabajos, Pagador, Factura, Datos_pagador, Pago, Universidad
from arbitrajes.models import Arbitro
from main_app.models import Rol,Sistema_asovac,Usuario_asovac, User, Usuario_rol_in_sistema, Area, Sub_area
# from trabajos.models import Detalle_version_final
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status
from trabajos.views import show_areas_modal

from .forms import EditAutorForm, DatosPagadorForm, PagoForm, FacturaForm, AdminCreateAutorForm, CreateUniversityForm, ImportFromExcelForm

from django.contrib import messages

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string


# Create your views here.
@login_required
def admin_create_author(request):
	if request.method == "POST":
		form = AdminCreateAutorForm(request.POST)
		print(form.is_valid(),"Ok")
		if form.is_valid():
			new_autor = form.save(commit = False)
			usuario = User(email = new_autor.correo_electronico, first_name = new_autor.nombres, last_name = new_autor.apellidos)
			username_base = (new_autor.nombres.split(' ')[0] + '.' + new_autor.apellidos.split(' ')[0]).lower()
			counter = 1
			username = username_base
			while User.objects.filter(username=username):
				username = username_base + str(counter)
				counter += 1

			usuario.username = username
			password = User.objects.make_random_password().lower()
			usuario.set_password(password)
			usuario.save()

			print(usuario.username)
			print(password)
			usuario_asovac = Usuario_asovac.objects.get(usuario = usuario)
			new_autor.usuario = usuario_asovac
			new_autor.save()

			rol = Rol.objects.get(id=5)
			sistema_asovac = Sistema_asovac.objects.get(id = request.session['arbitraje_id'])
			usuario_rol_in_sistema = Usuario_rol_in_sistema(rol = rol, sistema_asovac = sistema_asovac, usuario_asovac = usuario_asovac)
			usuario_rol_in_sistema.save()

			subarea= request.POST.getlist("subarea_select")
			for item in subarea:
				usuario_asovac.sub_area.add(Sub_area.objects.get(id=item))
			usuario_asovac.save()

			#Creación de instancia de arbitro
			new_arbitro = Arbitro(usuario = usuario_asovac, nombres = new_autor.nombres, apellidos = new_autor.apellidos, genero = new_autor.genero, cedula_pasaporte = new_autor.cedula_pasaporte, correo_electronico = new_autor.correo_electronico, telefono_habitacion_celular = new_autor.telefono_habitacion_celular )
			new_arbitro.save()
			context = {
			'username': username,
			'sistema_asovac': sistema_asovac.nombre,
			'password': password,
			'arbitraje': sistema_asovac,
			}
			msg_plain = render_to_string('../templates/email_templates/admin_create_author.txt', context)
			msg_html = render_to_string('../templates/email_templates/admin_create_author.html', context)
			send_mail(
					'Creación de usuario',         #titulo
					msg_plain,                          #mensaje txt
					config('EMAIL_HOST_USER'),          #email de envio
					[usuario.email],               #destinatario
					html_message=msg_html,              #mensaje en html
					)
			return redirect('autores:authors_list')
	else:
		form = AdminCreateAutorForm()


	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


	# print (rol_id)
	event_id = request.session['arbitraje_id']
	arbitraje = Sistema_asovac.objects.get(pk=event_id)
	estado = arbitraje.estado_arbitraje
	rol_id=get_roles(request.user.id , event_id)

	item_active = 2
	items = validate_rol_status(estado,rol_id,item_active,event_id)

	route_conf = get_route_configuracion(estado,rol_id,event_id)
	route_seg = get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, event_id)

	# print items

	areas= Area.objects.all()
	subareas= Sub_area.objects.all()
	context = {
		"nombre_vista": 'Administración - Crear Autor',
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
        'form': form,
        'areas':areas,
        'subareas':subareas
    }
	return render(request,"autores_admin_create_author.html",context)



@login_required
def autores_pag(request):
    context = {
        "nombre_vista": 'autores'
    }
    return render(request,"test_views.html",context)



@login_required
def authors_list(request):

	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
							{'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
							{'title':'Resultados',      'icon': 'fa-chart-area','active': False},
							{'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	# request.session para almacenar el item seleccionado del sidebar
	request.session['sidebar_item'] = "Autores"


	# print (rol_id)

	arbitraje_id = request.session['arbitraje_id']
	arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
	estado = arbitraje.estado_arbitraje
	rol_id=get_roles(request.user.id , arbitraje_id)

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


@login_required
def universitys_list(request):

	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
							{'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
							{'title':'Resultados',      'icon': 'fa-chart-area','active': False},
							{'title':'Administración',  'icon': 'fa-archive',   'active': False}]

	# request.session para almacenar el item seleccionado del sidebar
	request.session['sidebar_item'] = "Universidades"


	# print (rol_id)

	arbitraje_id = request.session['arbitraje_id']
	arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
	estado = arbitraje.estado_arbitraje
	rol_id=get_roles(request.user.id , arbitraje_id)

	item_active = 2
	items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

	route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

	# print items

	context = {
		'nombre_vista' : 'Universidades',
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
	return render(request, 'autores_universitys_list.html', context)

@login_required
def list_universitys(request):
    response = {}
    response['query'] = []
    arbitraje_id = request.session['arbitraje_id']
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
        if sort == 'fields.nombre':
            order='nombre'
        else:
            if sort == 'fields.facultad':
                order='facultad'
            else:
                order=sort
    else:
        if sort == 'fields.nombre':
            order='-nombre'
        else:
            if sort == 'fields.facultad':
                order='-facultad'
            else:
                order='-'+sort

    if search != "":
        data = Universidad.objects.filter( Q(nombre__icontains=search) | Q(facultad__icontains=search) | Q(escuela__icontains=search)).order_by(order)[init:limit]
        total = Universidad.objects.filter( Q(nombre__icontains=search) | Q(facultad__icontains=search) | Q(escuela__icontains=search)).count()
    else:
        if request.POST.get('limit', False) == False or request.POST.get('offset', False) == False:
            print "consulta para exportar"
            data = Universidad.objects.all().order_by(order)
            total = Universidad.objects.all().count()
        else:
            print "consulta normal"
            data = Universidad.objects.all().order_by(order)[init:limit]
            total = Universidad.objects.all().count()


	
    for item in data:
		if Autor.objects.filter(universidad = item).exists():
			can_delete = 0
		else:
			can_delete = 1
		response['query'].append({'id':item.id, 'nombre':item.nombre,'facultad': item.facultad,'escuela': item.escuela, 'can_delete': can_delete})
    response={
        'total': total,
        'query': response,
    }

    return JsonResponse(response)

@login_required
def delete_university(request, university_id):
    
    data = dict()
    universidad = get_object_or_404(Universidad, id = university_id)
    if request.method == "POST":
        universidad.delete()
        messages.success(request, "Universidad eliminada con éxito")
        return redirect('autores:universitys_list') 
    else:
        context = {
            'universidad':universidad,
        }
        data['html_form'] = render_to_string('ajax/university_delete.html',context,request=request)
    return JsonResponse(data)

@login_required
def details_university(request, university_id):
    
    data = dict()
    universidad = get_object_or_404(Universidad, id = university_id)
    context = {
		'universidad':universidad,
	}
    data['html_form'] = render_to_string('ajax/university_details.html',context,request=request)
    return JsonResponse(data)


@login_required
#Modal para crear universidad, ya teniendo los datos del autor en sesion serializados
def edit_university(request, university_id):
	data = dict()
	universidad = get_object_or_404(Universidad, id = university_id)
	if request.method == "POST":
		form = CreateUniversityForm(request.POST, instance = universidad)
		if form.is_valid():
			universidad = form.save()
			messages.success(request, 'La universidad se ha editado con éxito.')
			data['form_is_valid'] = True
			data['url'] = reverse('autores:universitys_list')
		else:
			data['form_is_valid'] = False
	else:
		form = CreateUniversityForm(instance = universidad)

	context ={
		'form': form,
		'creation': False,
		'universidad': universidad
	}
	data['html_form'] = render_to_string('ajax/university_form.html', context, request=request)
	return JsonResponse(data)

@login_required
#Modal para crear universidad, ya teniendo los datos del autor en sesion serializados
def create_university(request):
	data = dict()
	if request.method == "POST":
		form = CreateUniversityForm(request.POST)
		if form.is_valid():
			universidad = form.save()
			messages.success(request, 'La universidad se ha creado con éxito.')
			data['form_is_valid'] = True
			data['url'] = reverse('autores:universitys_list')
		else:
			data['form_is_valid'] = False
	else:
		form = CreateUniversityForm()

	context ={
		'form': form,
		'creation': True, 
	}
	data['html_form'] = render_to_string('ajax/university_form.html', context, request=request)
	return JsonResponse(data)

@login_required
def list_authors (request):
    response = {}
    temporal_list = []
    total = 0
    response['query'] = []
    arbitraje_id = request.session['arbitraje_id']
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
        data=Autor.objects.filter( Q(nombres__icontains=search) | Q(apellidos__icontains=search) | Q(cedula_pasaporte__icontains=search) | Q(correo_electronico__icontains=search) | Q(universidad__nombre__icontains=search)).order_by(order)#[:limit]
    else:
        if request.POST.get('limit', False) == False or request.POST.get('offset', False) == False:
            print "consulta para exportar"
            print Autor.objects.all().order_by(order).query
            data=Autor.objects.all().order_by(order)
        else:
            print "consulta normal"
            data=Autor.objects.all().order_by(order)


	
    for item in data:
        if(Usuario_rol_in_sistema.objects.filter(sistema_asovac = arbitraje_id, usuario_asovac = item.usuario, rol = 5).exists()):	
			temporal_list.append({'id':item.id, 'nombres':item.nombres,'apellidos': item.apellidos,'correo_electronico': item.correo_electronico, 'cedula_pasaporte': item.cedula_pasaporte,'universidad': item.universidad.nombre })
			total += 1
	response['query'] = temporal_list[init:limit:1]
    response={
        'total': total,
        'query': response,
    }

    return JsonResponse(response)



@login_required
def author_edit(request, autor_id):
	autor = get_object_or_404(Autor, id = autor_id)
	if request.method == 'POST':
		form = EditAutorForm(request.POST,user = autor.usuario.usuario, instance = autor)
		user = autor.usuario.usuario
		autor = Autor.objects.filter(nombres = user.first_name)
		print(autor)
		print(form.is_valid())
		if form.is_valid():
			try:
				autor = form.save()
				user_id = autor.usuario.usuario.id
				user = User.objects.get(id = user_id)
				user.first_name = autor.nombres
				user.last_name = autor.apellidos
				user.save()
				return redirect('autores:authors_list')
			except:
				pass
	else:
		form = EditAutorForm(user= autor.usuario.usuario,instance = autor)

	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


	arbitraje_id = request.session['arbitraje_id']
	arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
	estado = arbitraje.estado_arbitraje
	rol_id=get_roles(request.user.id , arbitraje_id)

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
        'form':form,
    }
	return render(request, 'autores_author_edit.html', context)



@login_required
def author_details(request, autor_id):
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


	# print (rol_id)
	arbitraje_id = request.session['arbitraje_id']
	arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
	estado = arbitraje.estado_arbitraje
	rol_id=get_roles(request.user.id,arbitraje_id)

	item_active = 2
	items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)
	rol_id=get_roles(request.user.id , arbitraje_id)

	route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
	route_seg= get_route_seguimiento(estado,rol_id)
	route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
	route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
	route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

	# print items
	autor = get_object_or_404(Autor, id = autor_id)
	context = {
		'nombre_vista' : 'Detalles del autor',
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
        'autor':autor,
    }
	return render(request, 'autores_details.html', context)



@login_required
#Modal para editar datos de autor del usuario logueado
def author_edit_modal(request, user_id):
	data = dict()
	user =  User.objects.get(id = user_id)
	autor = Autor.objects.get(usuario__usuario = user)
	form =	EditAutorForm(user= user,instance = autor)
	if request.method == "POST":
		# Este formulario tiene todas las opciones populadas de acuerdo al formulario enviado por POST.
		form = EditAutorForm(request.POST,user=user, instance = autor)
        if form.is_valid():
			try:
				autor = form.save()
				user.first_name = autor.nombres
				user.last_name = autor.apellidos
				user.email = autor.correo_electronico
				user.save()
				messages.success(request, 'Sus cambios al trabajo han sido guardados con éxito.')
				data['form_is_valid']= True
			except:
				pass
	context ={
		'form': form,
	}
	data['html_form'] = render_to_string('ajax/edit_own_author.html', context, request=request)
	return JsonResponse(data)

#Modal para ver los detalles del autor
@login_required
def author_details(request, autor_id):
	data = dict()
	#user =  User.objects.get(id = user_id)
	autor =  get_object_or_404(Autor, id = autor_id)
	context ={
		'autor': autor,
	}
	data['html_form'] = render_to_string('ajax/autores_details.html', context, request=request)
	return JsonResponse(data)



@login_required
#Vista para generar certificado
def generar_certificado(request):
	context={
		"nombre_vista": 'Generar Certificado'
	}
	return render(request,"autores_generar_certificado.html", context)



@login_required
#Vista donde el autor ve los pagadores de sus trabajos y tiene opción de añadir nuevos
def postular_trabajo(request, trabajo_id):
	main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


	# print (rol_id)
	event_id = request.session['arbitraje_id']
	arbitraje = Sistema_asovac.objects.get(pk=event_id)
	estado = arbitraje.estado_arbitraje
	rol_id=get_roles(request.user.id , event_id)

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
	autor_trabajo = Autores_trabajos.objects.get(autor = autor, sistema_asovac = sistema_asovac, trabajo = trabajo_id )

	facturas = Factura.objects.filter(pagador__autor_trabajo__trabajo = trabajo_id)

	print facturas
	context = {
		"nombre_vista": 'Postular Trabajo',
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
		'autor_trabajo': autor_trabajo,
		'facturas': facturas
    }
	return render(request,"autores_postular_trabajo.html",context)



@login_required
#Modal para crear datos del pagador
def postular_trabajo_pagador_modal(request, autor_trabajo_id,step):
	data = dict()
	autor_trabajo = get_object_or_404(Autores_trabajos, id = autor_trabajo_id)
	sistema = request.session['arbitraje_id']
	datos_pagador_form = DatosPagadorForm()
	factura_form = FacturaForm(sistema_id = sistema)
	pago_form = PagoForm(sistema_id = sistema)
	if request.method == "POST":
		if(step == '1'):	
			datos_pagador_form = DatosPagadorForm(request.POST)
			factura_form = FacturaForm(sistema_id = sistema)
			pago_form = PagoForm(sistema_id = sistema)
		elif(step == '2'):
			datos_pagador_form = DatosPagadorForm(request.POST)
			factura_form = FacturaForm(request.POST, sistema_id = sistema)
			pago_form = PagoForm(sistema_id = sistema)
		elif(step == '3'):
			datos_pagador_form = DatosPagadorForm(request.POST)
			factura_form = FacturaForm(request.POST, sistema_id = sistema)
			pago_form = PagoForm(request.POST, request.FILES, sistema_id = sistema)
			
		if datos_pagador_form.is_valid() and step == "1":
			step = "2"
		elif datos_pagador_form.is_valid() and factura_form.is_valid() and step =="2":
			step = "3"
		elif datos_pagador_form.is_valid() and factura_form.is_valid() and pago_form.is_valid() and step =="3":
			datos_pagador = datos_pagador_form.save()
			pagador = Pagador(autor_trabajo = autor_trabajo, datos_pagador = datos_pagador)
			pagador.save()
			pago = pago_form.save(commit=False)
			pago.numero_cuenta_origen = pago.numero_cuenta_origen.replace("-","")
			pago.save()
			factura = factura_form.save(commit=False)
			factura.pagador = pagador
			factura.pago = pago
			factura.iva = factura.monto_total * autor_trabajo.sistema_asovac.porcentaje_iva / 100
			factura.monto_subtotal = factura.monto_total - factura.iva
			factura.save()
			autor_trabajo.monto_total = autor_trabajo.monto_total - factura.monto_total
			if autor_trabajo.monto_total <= 0:
				autor_trabajo.pagado = True
				autor_trabajo.esperando_modificacion_pago = False
			autor_trabajo.save()
			#Código para actualizar estados de las otras instancias de autor_trabajo
			autores_trabajo_list = Autores_trabajos.objects.filter(trabajo = autor_trabajo.trabajo)
			for autor_trabajo_to_update in autores_trabajo_list:
				autor_trabajo_to_update.monto_total = autor_trabajo.monto_total
				autor_trabajo_to_update.pagado = autor_trabajo.pagado
				autor_trabajo_to_update.esperando_modificacion_pago = autor_trabajo.esperando_modificacion_pago
				autor_trabajo_to_update.save()
			messages.success(request, 'Pago añadido con éxito.')
			data['url'] = reverse('autores:postular_trabajo', kwargs={'trabajo_id':autor_trabajo.trabajo.id })
			data['form_is_valid'] = True
		elif step =="3":
			messages.error(request,"Número de referencia duplicado, por favor verifique el número de transferencia/cheque indicado dado que ya hay un pago registrado con ese número de referencia en nuestro sistema.")
	else:
		step = 1
	context ={
		'datos_pagador_form': datos_pagador_form,
		'factura_form': factura_form,
		'pago_form': pago_form,
		'autor_trabajo': autor_trabajo,
		'step': step
	}
	data['html_form'] = render_to_string('ajax/postular_trabajo_datos_pagador.html', context, request=request)
	return JsonResponse(data)


#Modal para ver los detalles del pago para postular un trabajo
@login_required
def detalles_pago(request, pagador_id):
	data = dict()
	#usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
	#autor = Autor.objects.get(usuario__usuario = request.user)
	#sistema_asovac = Sistema_asovac.objects.get(id = event_id)
	#pagador = get_object_or_404(Pagador, id = pagador_id)
	event_id = request.session['arbitraje_id']
	factura = get_object_or_404(Factura, pagador = pagador_id)
	autor_trabajo = get_object_or_404(Autores_trabajos ,autor__usuario__usuario = request.user, sistema_asovac = event_id, trabajo = factura.pagador.autor_trabajo.trabajo)
	context ={
		'factura': factura,
	}
	data['html_form'] = render_to_string('ajax/postular_trabajo_pay_details.html', context, request=request)
	return JsonResponse(data)


#Modal para ver los detalles del pago para postular un trabajo
@login_required
def detalles_rechazo_pago(request, factura_id):
	data = dict()
	event_id = request.session['arbitraje_id']
	factura = get_object_or_404(Factura, id = factura_id)
	autor_trabajo = get_object_or_404(Autores_trabajos ,autor__usuario__usuario = request.user, sistema_asovac = event_id, trabajo = factura.pagador.autor_trabajo.trabajo)
	context ={
		'factura': factura,
	}
	data['html_form'] = render_to_string('ajax/factura_observations.html', context, request=request)
	return JsonResponse(data)


@login_required
#Modal para crear universidad, ya teniendo los datos del autor en sesion serializados
def create_university_modal(request):
	data = dict()

	if request.method == "POST":
		form = CreateUniversityForm(request.POST)
		if form.is_valid():
			universidad = form.save()
			autor = serializers.json.Deserializer(request.session['autor']).next().object
			autor.universidad = universidad
			autor.save()
			request.session['is_author_created'] = True  
			data['url'] = reverse('trabajos:trabajos')
			data['form_is_valid'] = True
		else:
			data['form_is_valid'] = False
	else:
		form = CreateUniversityForm()

	context ={
		'form': form,
	}
	data['html_form'] = render_to_string('ajax/create_university.html', context, request=request)
	return JsonResponse(data)



#---------------------------------------------------------------------------------#
#                Guarda el archivo en la carpeta del proyecto                     #
#---------------------------------------------------------------------------------#
def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    # print "Nombre del archivo a guardar: ",filename
    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)



@login_required
# Para guardar el archivo recibido del formulario
def save_file(request,type_load):

    name= str(request.FILES.get('file'))
    file_name=''

    if type_load == "autores":
        extension = name.split('.')
        file_name= "cargaAutores."+extension[1]
        # Permite guardar el archivo y asignarle un nombre
        handle_uploaded_file(request.FILES['file'], file_name)
        route= "upload/"+file_name
    # print "Ruta del archivo: ",route
    return route



# Para obtener la extension del archivo
def get_extension_file(filename):

    extension = filename.split('.')
    return extension[1]



#---------------------------------------------------------------------------------#
#                Valida el contenido del excel para cargar usuarios               #
#---------------------------------------------------------------------------------#
def validate_alpha(cadena):
	valid_cadena = 1
	for char in cadena:
		if not char.isalpha() and char !=' ':
			valid_cadena = 0
	return valid_cadena



def validate_load_users(filename,extension,arbitraje_id):
	data= dict()
	data['status']=400
	data['message']="La estructura del archivo no es correcta"
	if extension == "xlsx" or extension == "xls":
		print "Formato xls/xlsx"
        book = xlrd.open_workbook(filename)

        if book.nsheets > 0:

            excel_file = book.sheet_by_index(0)

            if excel_file.ncols == 20:
                data['status']=200
                data['message']=""

                # se validan los campos del documento
                for fila in range(excel_file.nrows):
                    # Para no buscar los titulos
                    if fila > 0:
                        print(fila)
                        if excel_file.cell_value(rowx=fila, colx=0) == '':
							data['status']=400
							data['message'] = data['message'] + "Error en la fila {0} el nombre es un campo obligatorio \n".format(fila)

                        else:
							nombres_is_valid = validate_alpha(str(excel_file.cell_value(rowx=fila, colx=0)).strip())
							if not nombres_is_valid:
								data['status']=400
								data['message'] = data['message'] + "Error en la fila {0} el campo de nombres, solo debe tener letras \n".format(fila)

						# Se verifica que el campo apellidos no esté vacio
                        if excel_file.cell_value(rowx=fila, colx=1) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} el apellido es un campo obligatorio \n".format(fila)

                        else:
							apellidos_is_valid = validate_alpha(str(excel_file.cell_value(rowx=fila, colx=1)).strip())
							if not apellidos_is_valid:
								data['status']=400
								data['message'] = data['message'] + "Error en la fila {0} el campo de apellidos, solo debe tener letras \n".format(fila)

						# Se verifica que el campo género no este vacio
                        if excel_file.cell_value(rowx=fila, colx=2) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} el género es un campo obligatorio \n".format(fila)

                        elif excel_file.cell_value(rowx=fila, colx=2) != 'M' and excel_file.cell_value(rowx=fila, colx=2) != 'F':
							data['status']=400
							data['message'] = data['message'] + "Error en la fila {0} el género debe ser 'M' o 'F' (verifique que esté en mayúsculas) \n".format(fila)

						# Se verifica que el campo cédula/pasaporte no este vacio
                        if excel_file.cell_value(rowx=fila, colx=3) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} la cédula/pasaporte es un campo obligatorio \n".format(fila)
                        else:
							cedula_pasaporte = str(excel_file.cell_value(rowx=fila, colx=3))
							if cedula_pasaporte[0] !='V' and cedula_pasaporte != 'P':
								data['status'] = 400
								data['message'] = data['message'] + "Error en la fila {0}, el campo cédula/pasaporte debe empezar por una letra V o P seguido del número \n".format(fila)

							elif not cedula_pasaporte[1:].isdigit():
								data['status'] = 400
								data['message'] = data['message'] + "Error en la fila {0} la cédula/pasaporte solamente debe tener números después de V o P \n".format(fila)

							elif Autor.objects.filter(cedula_pasaporte = cedula_pasaporte).exists():
								data['status'] = 400
								data['message'] = data['message'] + "Error en la fila {0} ya existe un autor con esta cédula o pasaporte \n".format(fila)

						# Se verifica que el campo correo electrónico no este vacio
                        if excel_file.cell_value(rowx=fila, colx=4) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} el correo electrónico es un campo obligatorio \n".format(fila)

                        else:
							correo_electronico = str(excel_file.cell_value(rowx=fila, colx=4))
							if User.objects.filter(email = correo_electronico).exists():
								data['status']=400
								data['message'] = data['message'] + "Error en la fila {0}, ya hay un autor registrado con este correo electrónico \n".format(fila)
						# Se verifica que el campo telefono de oficina no este vacio
                        if excel_file.cell_value(rowx=fila, colx=5) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} el teléfono de oficina es un campo obligatorio \n".format(fila)

                        else:
							telefono_oficina = str(excel_file.cell_value(rowx=fila, colx=5)).split('.')
							telefono_oficina = telefono_oficina[0]
							telefono_oficina_length = len(telefono_oficina)
							if not telefono_oficina.isdigit():
								data['status']=400
								data['message'] = data['message'] + "Error en la fila {0}, el teléfono de oficina debe contener solamente dígitos \n".format(fila)

							elif telefono_oficina_length < 10 or 15 < telefono_oficina_length:
								data['status']=400
								data['message'] = data['message'] + "Error en la fila {0}, el teléfono de oficina debe tener de 10 a 15 dígitos \n".format(fila)

						# Se verifica que el campo teléfono de habitación/celular no este vacio
                        if excel_file.cell_value(rowx=fila, colx=6) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} el teléfono de habitación/celular es un campo obligatorio \n".format(fila)

                        else:
							telefono_habitacion_celular = str(excel_file.cell_value(rowx=fila, colx=6)).split('.')
							telefono_habitacion_celular = telefono_habitacion_celular[0]
							telefono_habitacion_celular_length = len(telefono_habitacion_celular)
							if not telefono_habitacion_celular.isdigit():
								data['status']=400
								data['message'] = data['message'] + "Error en la fila {0}, el teléfono de habitación/celular debe contener solamente dígitos \n".format(fila)

							elif telefono_habitacion_celular_length < 10 or 15 < telefono_habitacion_celular_length:
								data['status']=400
								data['message'] = data['message'] + "Error en la fila {0}, el teléfono de habitación/celular debe tener de 10 a 15 dígitos \n".format(fila)

						# Se verifica que el campo es miembro asovac no este vacio
                        if excel_file.cell_value(rowx=fila, colx=8) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} el '¿es miembro asovac?' es un campo obligatorio \n".format(fila)

                        elif excel_file.cell_value(rowx=fila, colx=8) != 'S' and excel_file.cell_value(rowx=fila, colx=8) != 'N':
							data['status']=400
							data['message'] = data['message'] + "Error en la fila {0}, el campo '¿es miembro asovac?' debe tener solo 'S' o 'N' \n".format(fila)

						# Se verifica que el campo nivel de instrucción no este vacio
                        if excel_file.cell_value(rowx=fila, colx=10) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} el nivel de instrucción es un campo obligatorio \n".format(fila)

						# Se verifica que el campo área no este vacio
                        if excel_file.cell_value(rowx=fila, colx=12) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} el área es un campo obligatorio \n".format(fila)

                        elif not Area.objects.filter(nombre__iexact = excel_file.cell_value(rowx=fila, colx=12).encode('utf-8').strip()).exists():
							data['status']=400
							data['message'] = data['message'] + "Error en la fila {0}, no existe un área con este nombre \n".format(fila)

						# Se verifica que el campo subarea1 no este vacio
                        if excel_file.cell_value(rowx=fila, colx=13) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} el subárea1 es un campo obligatorio \n".format(fila)

                        else:
							area = Area.objects.get(nombre__iexact = excel_file.cell_value(rowx=fila, colx=12).encode('utf-8').strip())
							subarea_name = excel_file.cell_value(rowx=fila, colx=13).encode('utf-8').strip()
							if not Sub_area.objects.filter(area = area, nombre__iexact = subarea_name).exists():
								data['status']=400
								data['message'] = data['message'] + "Error en la fila {0}, no hay subarea1 asociada al área de {1} con el nombre indicado \n".format(fila, area.nombre)

						# Se verifica que el campo subarea2 sea correcto en el caso que tenga datos
                        if excel_file.cell_value(rowx=fila, colx=14) != '' and not Sub_area.objects.filter(area = area, nombre__iexact = excel_file.cell_value(rowx=fila, colx=14).encode('utf-8').strip()).exists():
							data['status']=400
							data['message'] = data['message'] + "Error en la fila {0}, no hay subarea2 asociada al área de {1} con el nombre indicado \n".format(fila, area.nombre)

						# Se verifica que el campo subarea3 sea correcto en el caso que tenga datos
                        if excel_file.cell_value(rowx=fila, colx=15) != '' and not Sub_area.objects.filter(area = area, nombre__iexact = excel_file.cell_value(rowx=fila, colx=15).encode('utf-8').strip()).exists():
							data['status']=400
							data['message'] = data['message'] + "Error en la fila {0}, no hay subarea3 asociada al área de {1} con el nombre indicado \n".format(fila, area.nombre)

						# Se verifica que el campo universidad no este vacio
                        if excel_file.cell_value(rowx=fila, colx=16) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} la universidad es un campo obligatorio \n".format(fila)

						# Se verifica que el facultad no este vacio
                        if excel_file.cell_value(rowx=fila, colx=17) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} la facultad es un campo obligatorio \n".format(fila)

						# Se verifica que el campo escuela no este vacio
                        if excel_file.cell_value(rowx=fila, colx=18) == '':
                            data['status']=400
                            data['message'] = data['message'] + "Error en la fila {0} la escuela es un campo obligatorio \n".format(fila)
						
                        if excel_file.cell_value(rowx=fila, colx=16) != '' and excel_file.cell_value(rowx=fila, colx=17) != '' and excel_file.cell_value(rowx=fila, colx=18) != '' and not Universidad.objects.filter(nombre__iexact = excel_file.cell_value(rowx=fila, colx=16).encode('utf-8').strip(), facultad__iexact = excel_file.cell_value(rowx=fila, colx=17).encode('utf-8').strip(), escuela__iexact = excel_file.cell_value(rowx=fila, colx=18).encode('utf-8').strip()).exists():
							data['status']=400
							data['message'] = data['message'] + "Error en la fila {0}, no hay registros en el sistema con esa universidad, facultad y escuela \n".format(fila)

						# Se verifica que el campo facultad no esté vacío



	# Inserta los registros una vez realizada la validación correspondiente
	if data['status'] == 200:
		is_create = create_authors(excel_file,arbitraje_id)
		print is_create
		if is_create == -1:
			data['message'] = "Los datos del archivo son válidos"
		else:
			data['status'] = 400
			data['message'] =  "Problemas en la fila {0} al momento de almacenar, porque ya hay un autor con esa cédula o correo electrónico. Se lograron importar los autores hasta la fila anterior, es decir, hasta la fila {1}.".format(is_create, is_create-1)
	return data



#---------------------------------------------------------------------------------#
#             Hecha la validación, se procede a la creación de los autores        #
#---------------------------------------------------------------------------------#
def create_authors(excel_file, arbitraje_id):

	resultado = -1

	for fila in range(excel_file.nrows):
		if fila > 0:
            # Guarda el usuario
			try:
				if not User.objects.filter(email = excel_file.cell_value(rowx=fila, colx=4).strip()).exists() or not Autor.objects.filter(cedula_pasaporte = excel_file.cell_value(rowx=fila, colx=3).strip()).exists():
					user= User()
					user.first_name = excel_file.cell_value(rowx=fila, colx=0).strip()
					user.last_name = excel_file.cell_value(rowx=fila, colx=1).strip()

					username_base = user.first_name.split(' ')[0].lower() + '.' + user.last_name.split(' ')[0].lower()
					counter = 1
					username = username_base

					while User.objects.filter(username=username):
						username = username_base + str(counter)
						counter += 1

					user.username = username
					password = User.objects.make_random_password().lower()
					user.set_password(password)

					user.email = excel_file.cell_value(rowx=fila, colx=4).strip()
					user.save()

					# Crear usuario_asovac
					usuario_asovac= Usuario_asovac.objects.get(usuario=user)
					arbitraje=Sistema_asovac.objects.get(id=arbitraje_id)
					rol_author = Rol.objects.get(id=5)

					usuario_rol_in_sistema = Usuario_rol_in_sistema(rol = rol_author, sistema_asovac = arbitraje, usuario_asovac = usuario_asovac)
					usuario_rol_in_sistema.save()

					area = Area.objects.get(nombre__iexact = excel_file.cell_value(rowx=fila, colx=12).strip())
					subarea1 = Sub_area.objects.get(area = area, nombre__iexact = excel_file.cell_value(rowx=fila, colx=13).strip())

					usuario_asovac.sub_area.add(subarea1)
					if excel_file.cell_value(rowx=fila, colx=14) != "":
						subarea2= Sub_area.objects.get(area = area, nombre__iexact = excel_file.cell_value(rowx=fila, colx=14).strip())
						usuario_asovac.sub_area.add(subarea2)

					if excel_file.cell_value(rowx=fila, colx=15) != "":
						subarea3= Sub_area.objects.get(area = area, nombre__iexact = excel_file.cell_value(rowx=fila, colx=15).strip())
						usuario_asovac.sub_area.add(subarea3)

					usuario_asovac.save()

					new_autor = Autor(usuario = usuario_asovac, nombres = user.first_name, apellidos = user.last_name, correo_electronico = user.email)
					if excel_file.cell_value(rowx=fila, colx=2).strip().lower() == "m":
						new_autor.genero = 0
					else:
						new_autor.genero = 1


					new_autor.cedula_pasaporte = excel_file.cell_value(rowx=fila, colx=3).strip()
					new_autor.telefono_oficina = str(excel_file.cell_value(rowx=fila, colx=5)).split('.')[0]
					new_autor.telefono_habitacion_celular = str(excel_file.cell_value(rowx=fila, colx=6)).split('.')[0]

					if excel_file.cell_value(rowx=fila, colx=7).strip() != '':
						new_autor.direccion_envio_correspondencia = excel_file.cell_value(rowx=fila, colx=7).strip()

					if excel_file.cell_value(rowx=fila, colx=8).strip().lower() == "s":
						new_autor.es_miembro_asovac = True
					else:
						new_autor.es_miembro_asovac = False

					if excel_file.cell_value(rowx=fila, colx=9).strip() != '':
						new_autor.capitulo_perteneciente = excel_file.cell_value(rowx=fila, colx=9).strip()

					new_autor.nivel_instruccion = excel_file.cell_value(rowx=fila, colx=10)

					if excel_file.cell_value(rowx=fila, colx=11).strip() != '':
						new_autor.observaciones = excel_file.cell_value(rowx=fila, colx=11).strip()
					new_autor.instituto_investigacion = excel_file.cell_value(rowx=fila, colx=19).strip()
					universidad = Universidad.objects.get(nombre__iexact = excel_file.cell_value(rowx=fila, colx=16).strip(), facultad__iexact = excel_file.cell_value(rowx=fila, colx=17).strip(), escuela__iexact = excel_file.cell_value(rowx=fila, colx=18).strip())
					new_autor.universidad = universidad
					new_autor.save()

					#Creación de instancia de arbitro
					new_arbitro = Arbitro(usuario = usuario_asovac, nombres = new_autor.nombres, apellidos = new_autor.apellidos, genero = new_autor.genero, cedula_pasaporte = new_autor.cedula_pasaporte, correo_electronico = new_autor.correo_electronico, telefono_habitacion_celular = new_autor.telefono_habitacion_celular )
					new_arbitro.save()

					context = {
						'username': username,
						'sistema_asovac': arbitraje.nombre,
						'password': password,
						'arbitraje': arbitraje,
					}
					msg_plain = render_to_string('../templates/email_templates/admin_create_author.txt', context)
					msg_html = render_to_string('../templates/email_templates/admin_create_author.html', context)
					send_mail(
							'Creación de usuario',         #titulo
							msg_plain,                          #mensaje txt
							config('EMAIL_HOST_USER'),          #email de envio
							[user.email],               #destinatario
							html_message=msg_html,              #mensaje en html
							)

				else:
					resultado = fila
					break;
			except:
				resultado = fila
				break;


	return resultado



@login_required
def load_authors_modal(request):
	data = dict()
	arbitraje_id = request.session['arbitraje_id']

	if request.method == "POST":
		form = ImportFromExcelForm(request.POST, request.FILES)
		if form.is_valid():
			# Para guardar el archivo de forma local
			file_name= save_file(request,"autores")
			extension= get_extension_file(file_name)

            #Valida el contenido del archivo
			response = validate_load_users(file_name, extension,arbitraje_id)
			print response

			if response['status'] == 200:
				messages.success(request, "La importación de autores fue llevada a cabo con éxito.")
				return redirect('autores:authors_list')
			else:
				filename = "Error-Log-Import.txt"
				content = response['message']
				response = HttpResponse(content, content_type='text/plain')
				response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
				return response

			#data['url'] = reverse('autores:authors_list')
			#data['form_is_valid'] = True
		else:
			#data['form_is_valid'] = False
			messages.error(request, "El archivo indicado no es xls o xlsx, por favor suba un archivo en alguno de esos dos formatos.")
			return redirect('autores:authors_list')
	else:
		form = ImportFromExcelForm()

	context ={
		'form': form,
	}
	data['html_form'] = render_to_string('ajax/load_authors.html', context, request=request)
	return JsonResponse(data)



#---------------------------------------------------------------------------------#
#                               Exportar Autores                                  #
#---------------------------------------------------------------------------------#
@login_required
def export_authors(request):

	arbitraje_id = request.session['arbitraje_id']
	data = []
	temporal_list = Usuario_rol_in_sistema.objects.filter(rol = 5, sistema_asovac = arbitraje_id)
	for item in temporal_list:
		if Autor.objects.filter(usuario = item.usuario_asovac).exists():
			data.append(Autor.objects.get(usuario = item.usuario_asovac))

	# Para definir propiedades del documento de excel
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Autores.xls'
	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet("Autores")
	# Para agregar los titulos de cada columna
	row_num = 0
	columns = ['Nombres (*)', 'Apellidos (*)','Género M/F (*)', 'Cédula/Pasaporte(*)','Correo Electrónico (*)', 'Teléfono de oficina(*)', 'Teléfono de habitación/celular(*)', 'Dirección de correspondencia', 'Es miembro asovac? S/N (*)', 'Capítulo perteneciente', 'Nivel de instrucción(*)', 'Observaciones','Área(*)','Subárea1(*)', 'Subárea2', 'Subárea3', 'Universidad(*)', 'Facultad(*)', 'Escuela(*)', 'Instituto de investigación']
	for col_num in range(len(columns)):
		worksheet.write(row_num, col_num, columns[col_num])

	for item in data:
		row_num += 1
		counter = 0
		user_subarea_list = item.usuario.sub_area.all()
		subarea1=''
		subarea2 = ''
		subarea3 = ''
		area = ''
		
		for subarea in user_subarea_list:
			if counter == 0:
				area = subarea.area.nombre
				subarea1 = subarea.nombre
			elif counter == 1:
				subarea2 = subarea.nombre
			elif counter == 2:
				subarea3 = subarea.nombre
			else:
				break
			counter += 1

		if item.genero == 0:
			genero = 'M'
		else:
			genero = 'F'

		if item.es_miembro_asovac == True:
			es_miembro_asovac = 'S'
		else:
			es_miembro_asovac = 'N'
		row = [item.nombres, item.apellidos, genero, item.cedula_pasaporte, item.correo_electronico, item.telefono_oficina, item.telefono_habitacion_celular, item.direccion_envio_correspondencia, es_miembro_asovac, item.capitulo_perteneciente, item.nivel_instruccion, item.observaciones, area, subarea1, subarea2, subarea3, item.universidad.nombre, item.universidad.facultad, item.universidad.escuela, item.instituto_investigacion ]
		for col_num in range(len(row)):
			worksheet.write(row_num, col_num, row[col_num])

	workbook.save(response)

	return response


#---------------------------------------------------------------------------------#
#                               Format para import de Autores                     #
#---------------------------------------------------------------------------------#
@login_required
def format_import_authors(request):

	arbitraje_id = request.session['arbitraje_id']
	data = []
	temporal_list = Usuario_rol_in_sistema.objects.filter(rol = 5, sistema_asovac = arbitraje_id)
	for item in temporal_list:
		if Autor.objects.filter(usuario = item.usuario_asovac).exists():
			data.append(Autor.objects.get(usuario = item.usuario_asovac))

	# Para definir propiedades del documento de excel
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Formato_Autores.xls'
	workbook = xlwt.Workbook()
	worksheet = workbook.add_sheet("Autores")
	# Para agregar los titulos de cada columna
	row_num = 0
	columns = ['Nombres (*)', 'Apellidos (*)','Género M/F (*)', 'Cédula/Pasaporte(*)','Correo Electrónico (*)', 'Teléfono de oficina(*)', 'Teléfono de habitación/celular(*)', 'Dirección de correspondencia', 'Es miembro asovac? S/N (*)', 'Capítulo perteneciente', 'Nivel de instrucción(*)', 'Observaciones','Área(*)','Subárea1(*)', 'Subárea2', 'Subárea3', 'Universidad(*)', 'Facultad(*)', 'Escuela(*)', 'Instituto de investigación']
	for col_num in range(len(columns)):
		worksheet.write(row_num, col_num, columns[col_num])
	
	row_num += 1
	columns = ['usuario', 'prueba', 'M', 'V9999999', 'prueba@gmail.com', '4249999999', '2129999999', 'El Valle', 'N', 'Caracas', 'Licenciado', 'X', 'Congreso de la Sociedad Venezolana de Física', 'Física de los Materiales', '', '', 'nombre', 'facultad', 'escuela','instituto' ]
	for col_num in range(len(columns)):
		worksheet.write(row_num, col_num, columns[col_num])

	row_num += 1
	columns = ['otrousuario', 'prueba', 'F', 'P9999999', 'prueba2@gmail.com', '4269999999', '2129999999', 'Altamira', 'S', 'Caracas', 'Postgrado', '', 'Congreso de la Sociedad Venezolana de Física', 'Física de los Materiales', 'Física del Espacio', '', 'nombre', 'facultad', 'escuela', '' ]
	for col_num in range(len(columns)):
		worksheet.write(row_num, col_num, columns[col_num])

	workbook.save(response)

	return response
