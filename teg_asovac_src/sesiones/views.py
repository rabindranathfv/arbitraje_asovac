# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decouple import config
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Sesion, Coordinadores_sesion, Espacio
from autores.models import Autores_trabajos, Autor
from main_app.models import Rol,Sistema_asovac,Usuario_asovac
from trabajos.models import Trabajo

from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render,get_object_or_404, redirect

from .forms import SesionForm, EspacioFisicoForm, EspacioVirtualForm

import datetime, operator
from datetime import datetime
# Create your views here.
@login_required
def sesiones_pag(request):
    context = {
        "nombre_vista": 'sesiones'
    }
    return render(request,"test_views.html",context)



####################### Inclusión de eventos en arbitrajes########################
@login_required
def sesions_list(request):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    
    context = {
        'nombre_vista' : 'Sesiones de arbitraje',
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
    return render(request,"sesiones_sesions_list.html",context)



@login_required
def list_sesions (request):
    response = {}
    response['query'] = []
    arbitraje_id = request.session['arbitraje_id']

    sort= request.POST['sort']
    if sort == "autor_2":
        sort = "autor"
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
        if sort == 'fields.sesion__nombre_sesion':
            order='sesion__nombre_sesion'
        else:
            if sort == 'fields.sesion__fecha_sesion':
                order='sesion__fecha_sesion'
            else:
                order=sort
    else:
        if sort == 'fields.sesion__nombre_sesion':
            order='-sesion__nombre_sesion'
        else:
            if sort == 'fields.sesion__fecha_sesion':
                order='-sesion__fecha_sesion'
            else:
                order='-'+sort

    if search != "":
        
        try: 
            in_time = datetime.strptime(search, "%I:%M %p")
            out_time = datetime.strftime(in_time, "%H:%M")
        except:
            out_time = search
        #data=Coordinadores_sesion.objects.filter( Q(sesion__sistema = arbitraje_id) & (Q(sesion__espacio__espacio_virtual__url_virtual__icontains = search) | Q(sesion__espacio__espacio_fisico__nombre__icontains = search) | Q(sesion__sistema = arbitraje_id) & (Q(sesion__nombre_sesion__icontains=search) | Q(sesion__fecha_sesion__icontains=search) | Q(sesion__modalidad__icontains = search) | Q(autor__nombres__icontains = search) | Q(autor__apellidos__icontains = search)))).order_by(order)[init:limit]
        data=Coordinadores_sesion.objects.filter( Q(sesion__sistema = arbitraje_id) & (Q(sesion__nombre_sesion__icontains=search) | Q(sesion__lugar__icontains=search) | Q(sesion__fecha_sesion__icontains = search) | Q(sesion__hora_inicio__icontains = out_time) | Q(sesion__hora_fin__icontains = out_time)| Q(autor__nombres__icontains = search) | Q(autor__apellidos__icontains = search))).order_by(order)[init:limit]
        total=Coordinadores_sesion.objects.filter( Q(sesion__sistema = arbitraje_id) & (Q(sesion__nombre_sesion__icontains=search) | Q(sesion__lugar__icontains=search) | Q(sesion__fecha_sesion__icontains = search) | Q(sesion__hora_inicio__icontains = out_time) | Q(sesion__hora_fin__icontains = out_time)| Q(autor__nombres__icontains = search) | Q(autor__apellidos__icontains = search))).distinct('sesion').count()
        
    else:
        if request.POST.get('limit', False) == False or request.POST.get('offset', False) == False:
            print "consulta para exportar"
            print Sesion.objects.all().order_by(order).query
            data = Sesion.objects.all().order_by(order)
            total = Sesion.objects.all().count()
        else:
            print "consulta normal"
            data = Coordinadores_sesion.objects.filter(sesion__sistema = arbitraje_id ).order_by(order)[init:limit]
            total = Coordinadores_sesion.objects.filter(sesion__sistema = arbitraje_id ).distinct('sesion').count()
    
    listed = []
    #total = 0
    for item in data:
        if not item.sesion.id in listed:
            coordinador = ''
            co_coordinador = ''
            #Query para obtener los coordinadores 
            for autor in item.sesion.coordinadores.all():
                coordinador_sesion = Coordinadores_sesion.objects.get(autor = autor, sesion = item.sesion)
                if coordinador_sesion.coordinador == True:
                    coordinador = autor.nombres.split(" ")[0] + ' ' + autor.apellidos.split(" ")[0]
                if coordinador_sesion.co_coordinador == True:
                    co_coordinador = autor.nombres.split(" ")[0] + ' ' + autor.apellidos.split(" ")[0]
            
            sesion_jobs = Autores_trabajos.objects.filter(es_autor_principal = True, trabajo__sesion = item.sesion).count()

            response['query'].append({'sesion__id':item.sesion.id, 'sesion__nombre_sesion': item.sesion.nombre_sesion, 'sesion__lugar': item.sesion.lugar, 'sesion__fecha_sesion': item.sesion.fecha_sesion.strftime("%Y-%m-%d"), 'sesion__hora_inicio': item.sesion.hora_inicio.strftime("%I:%M %p"), 'sesion__hora_fin': item.sesion.hora_fin.strftime("%I:%M %p") , 'autor': coordinador, 'autor_2': co_coordinador, 'sesion_jobs': sesion_jobs  })
            listed.append(item.sesion.id)

    response={
        'total': total,
        'query': response,
    }

    return JsonResponse(response)



@login_required
def sesions_edit(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol_id=get_roles(request.user.id)

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
    return render(request, 'sesiones_sesions_edit.html', context)



@login_required
def sesions_space_list(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol_id=get_roles(request.user.id)

    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']

    item_active = 4
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
    return render(request, 'sesiones_space_list.html', context)



@login_required
def sesions_space_edit(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol_id=get_roles(request.user.id)

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
    return render(request, 'sesiones_space_edit.html', context)



####################### Inclusión de eventos en arbitrajes########################
@login_required
def create_sesion(request):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 5
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
   
    virtual_selected = False
    
    if request.method == 'POST': 
        """
        modalidad = request.POST.get('modalidad_select')
        if modalidad == "1":
            sesion_form = SesionForm(request.POST)
            espacio_form = EspacioFisicoForm(request.POST)
            if sesion_form.is_valid() and espacio_form.is_valid():
                espacio_fisico = espacio_form.save()
                
                espacio = Espacio(espacio_fisico = espacio_fisico, fecha_ocupacion = sesion_form.cleaned_data['fecha_ocupacion'], tipo_espacio = "Físico")
                espacio.save()
                
                sesion = sesion_form.save(commit = False)
                sesion.sistema = arbitraje
                sesion.espacio = espacio
                sesion.modalidad = "Presencial"
                sesion.save()

                coordinador_sesion = Coordinadores_sesion(sesion = sesion)
                coordinador_sesion.save()
                
                messages.success(request, "Sesion con espacio físico creada con éxito.")
                return redirect('sesiones:sesions_list')
        else:
            sesion_form = SesionForm(request.POST)
            espacio_form = EspacioVirtualForm(request.POST)
            if sesion_form.is_valid() and espacio_form.is_valid():
                espacio_virtual = espacio_form.save()

                espacio = Espacio(espacio_virtual = espacio_virtual, fecha_ocupacion = sesion_form.cleaned_data['fecha_ocupacion'], tipo_espacio = "Virtual")
                espacio.save()

                sesion = sesion_form.save(commit = False)
                sesion.sistema = arbitraje
                sesion.espacio = espacio
                sesion.modalidad = "Presencial"
                sesion.save()

                coordinador_sesion = Coordinadores_sesion(sesion = sesion)
                coordinador_sesion.save()

                messages.success(request, "Sesion con espacio virtual creada con éxito.")
                return redirect('sesiones:sesions_list')
            else:
                virtual_selected = True
        """
        sesion_form = SesionForm(request.POST)
        if sesion_form.is_valid():
            sesion = sesion_form.save(commit = False)
            sesion.sistema = arbitraje
            sesion.save()

            coordinador_sesion = Coordinadores_sesion(sesion = sesion)
            coordinador_sesion.save()
            
            messages.success(request, "Sesión creada con éxito.")
            return redirect('sesiones:sesions_list')
    else:
        sesion_form = SesionForm()
    
    context = {
        'nombre_vista' : 'Sesiones de arbitraje',
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
        'sesion_form': sesion_form,
        'virtual_selected': virtual_selected
    }
    return render(request,"sesiones_create_sesion.html",context)



@login_required
def load_space_form(request, modalidad):
    data = dict()
    #Modalidad = 1 es espacio físico, modalidad = 2 es espacio virtual
    if modalidad == "1":
        form = EspacioFisicoForm()
    else:
        form = EspacioVirtualForm()
    context = {'form': form,}
    data['html_select'] = render_to_string('ajax/form.html', context, request = request)
    return JsonResponse(data)



@login_required
def delete_sesion(request, sesion_id):
    
    data = dict()
    sesion = get_object_or_404(Sesion, id = sesion_id)
    if request.method == "POST":
        sesion.delete()
        messages.success(request, "Sesión eliminada con éxito")
        return redirect('sesiones:sesions_list') 
    else:
        context = {
            'sesion':sesion,
        }
        data['html_form'] = render_to_string('ajax/sesion_delete.html',context,request=request)
    return JsonResponse(data)


def details_sesion(request, sesion_id):
    
    data = dict()
    sesion = get_object_or_404(Sesion, id = sesion_id)
    
    coordinador = Coordinadores_sesion.objects.filter(sesion = sesion, coordinador = True).first()
    co_coordinador = Coordinadores_sesion.objects.filter(sesion = sesion, co_coordinador = True).first()
    if coordinador:
        coordinador = coordinador.autor.nombres + ' ' + coordinador.autor.apellidos
    else:
        coordinador = ''
    
    if co_coordinador:
        co_coordinador = co_coordinador.autor.nombres + ' ' + co_coordinador.autor.apellidos
    else:
        co_coordinador = ''

    context = {
        'sesion':sesion,
        'coordinador': coordinador,
        'co_coordinador': co_coordinador
    }
    data['html_form'] = render_to_string('ajax/sesion_details.html',context,request=request)
    return JsonResponse(data)
 

def edit_sesion(request, sesion_id):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 5
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
   
    sesion = get_object_or_404(Sesion, id = sesion_id)
    modo_edicion = True
    if request.method == 'POST': 
        sesion_form = SesionForm(request.POST, instance = sesion)
        if sesion_form.is_valid():
            sesion = sesion_form.save()
            
            messages.success(request, 'Sesión editada con éxito')
            return redirect('sesiones:sesions_list')
    else:
        sesion_form = SesionForm(instance = sesion, initial = { 'hora_inicio': sesion.hora_inicio.strftime("%I:%M %p"), 'hora_fin': sesion.hora_fin.strftime("%I:%M %p")})
    context = {
        'nombre_vista' : 'Editar sesión',
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
        'sesion_form': sesion_form,
        'sesion': sesion,
        'modo_edicion': modo_edicion
    }
    return render(request,"sesiones_create_sesion.html",context)


def sesion_job_list(request, sesion_id):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    sesion = get_object_or_404(Sesion, id = sesion_id)
    
    have_coordinator = Coordinadores_sesion.objects.filter(sesion = sesion, coordinador = True).exists()
    if have_coordinator:
       have_coordinator = 1
       coordinator_id = Coordinadores_sesion.objects.filter(sesion = sesion, coordinador = True).first().autor.id
    else:
        have_coordinator = 0
        coordinator_id = 0
    
    have_cocoordinator = Coordinadores_sesion.objects.filter(sesion = sesion, co_coordinador = True).exists()
    if have_cocoordinator:
        have_cocoordinator = 1
        cocoordinator_id = Coordinadores_sesion.objects.filter(sesion = sesion, co_coordinador = True).first().autor.id
    else:
        have_cocoordinator = 0
        cocoordinator_id = 0
    context = {
        'nombre_vista' : 'Sesiones de arbitraje',
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
        'sesion': sesion,
        'have_coordinator': have_coordinator,
        'coordinator_id': coordinator_id,
        'have_cocoordinator': have_cocoordinator,
        'cocoordinator_id': cocoordinator_id
    }
    return render(request,"sesiones_sesion_job_list.html",context)

def list_job_sesion (request, sesion_id):
    response = {}
    response['query'] = []
    arbitraje_id = request.session['arbitraje_id']
    sistema_asovac = get_object_or_404(Sistema_asovac, id = arbitraje_id)
    sesion = get_object_or_404(Sesion, id = sesion_id, sistema = sistema_asovac)
    
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
        if sort == 'fields.trabajo__titulo_espanol':
            order='trabajo__titulo_espanol'
        else:
            if sort == 'fields.autor__cedula_pasaporte':
                order='autor__cedula_pasaporte'
            else:
                order=sort
    else:
        if sort == 'fields.trabajo__titulo_espanol':
            order='-trabajo__titulo_espanol'
        else:
            if sort == 'fields.autor__cedula_pasaporte':
                order='-autor__cedula_pasaporte'
            else:
                order='-'+sort

    if search != "":
        data = Autores_trabajos.objects.filter(Q(sistema_asovac = sistema_asovac) & Q(es_ponente = True) & Q(trabajo__sesion = sesion) & (Q(trabajo__titulo_espanol__icontains = search) | Q(autor__cedula_pasaporte__icontains = search) | Q(autor__correo_electronico__icontains = search) | Q(autor__nivel_instruccion__icontains = search))).order_by(order)[init:limit]
        total= Autores_trabajos.objects.filter(Q(sistema_asovac = sistema_asovac) & Q(es_ponente = True) & Q(trabajo__sesion = sesion) & (Q(trabajo__titulo_espanol__icontains = search) | Q(autor__cedula_pasaporte__icontains = search) | Q(autor__correo_electronico__icontains = search) | Q(autor__nivel_instruccion__icontains = search))).count()
        
    else:
        if request.POST.get('limit', False) == False or request.POST.get('offset', False) == False:
            print "consulta para exportar"
            data = Autores_trabajos.objects.filter(sistema_asovac = sistema_asovac, es_ponente = True, trabajo__sesion = sesion).order_by(order)
            total = Autores_trabajos.objects.filter(sistema_asovac = sistema_asovac, es_ponente = True, trabajo__sesion = sesion).count()
        else:
            print "consulta normal"
            data = Autores_trabajos.objects.filter(sistema_asovac = sistema_asovac, es_ponente = True, trabajo__sesion = sesion).order_by(order)[init:limit]
            total = Autores_trabajos.objects.filter(sistema_asovac = sistema_asovac, es_ponente = True, trabajo__sesion = sesion).count()
    
    listed = []
    #total = 0
    for item in data:
        if item.autor.nivel_instruccion == "Universidad" or item.autor.nivel_instruccion == "Postgrado":
            posible_coordinador = True
        else:
            posible_coordinador = False
        
        response['query'].append({'trabajo__id': item.trabajo.id, 
                                'autor__id': item.autor.id,
                                'trabajo__titulo_espanol': item.trabajo.titulo_espanol,
                                'autor__cedula_pasaporte': item.autor.cedula_pasaporte,
                                'autor__correo_electronico': item.autor.correo_electronico,
                                'autor__nivel_instruccion': item.autor.nivel_instruccion,
                                'posible_coordinador': posible_coordinador })

    response={
        'total': total,
        'query': response,
    }

    return JsonResponse(response)





def assign_coordinator(request, sesion_id, autor_id):
    data = dict()
    sesion = get_object_or_404(Sesion, id = sesion_id)

    autor = get_object_or_404(Autor, id = autor_id)

    if request.method == "POST":
        coordinador_sesion = Coordinadores_sesion.objects.filter(sesion = sesion, coordinador = True).first()
        if coordinador_sesion:
            coordinador_sesion.autor = autor
        else:
            coordinador_sesion = Coordinadores_sesion.objects.filter(sesion = sesion, coordinador = False, co_coordinador = False).first()
            if coordinador_sesion:
                coordinador_sesion.autor = autor 
                coordinador_sesion.coordinador = True
            else:
                coordinador_sesion = Coordinadores_sesion(sesion = sesion, autor = autor, coordinador = True)
        
        coordinador_sesion.save()

        old_coordinador_sesion = Coordinadores_sesion.objects.filter(sesion = sesion, autor = autor, co_coordinador = True).first()
        if old_coordinador_sesion:
            old_coordinador_sesion.delete()

        messages.success(request, "El coordinador fue asignado con éxito")
        
        context = {
            'sesion': coordinador_sesion.sesion,
            'cargo': "coordinador",
            'arbitraje': sesion.sistema,
        }
        msg_plain = render_to_string('../templates/email_templates/coordinator_assign.txt', context)
        msg_html = render_to_string('../templates/email_templates/coordinator_assign.html', context)

        send_mail(
                'Asignación como coordinador',         #titulo
                msg_plain,                          #mensaje txt
                config('EMAIL_HOST_USER'),          #email de envio
                [coordinador_sesion.autor.correo_electronico],               #destinatario
                html_message=msg_html,              #mensaje en html
                )

        return redirect('sesiones:sesions_list')

    context = {
        'sesion': sesion,
        'autor': autor
    }
    data['html_form'] = render_to_string('ajax/sesiones_assign_coordinator.html',context,request=request)
    return JsonResponse(data)

def assign_co_coordinator(request, sesion_id, autor_id):
    data = dict()
    sesion = get_object_or_404(Sesion, id = sesion_id)

    autor = get_object_or_404(Autor, id = autor_id)

    if request.method == "POST":
        co_coordinador_sesion = Coordinadores_sesion.objects.filter(sesion = sesion, co_coordinador = True).first()
        if co_coordinador_sesion:
            co_coordinador_sesion.autor = autor
        else:
            co_coordinador_sesion = Coordinadores_sesion.objects.filter(sesion = sesion, coordinador = False, co_coordinador = False).first()
            if co_coordinador_sesion:
                co_coordinador_sesion.autor = autor 
                co_coordinador_sesion.co_coordinador = True
            else:
                co_coordinador_sesion = Coordinadores_sesion(sesion = sesion, autor = autor, co_coordinador = True)
        
        co_coordinador_sesion.save()

        coordinador_sesion = Coordinadores_sesion.objects.filter(sesion = sesion, autor = autor, coordinador = True).first()
        if coordinador_sesion:    
            coordinador_sesion.delete()
        
        messages.success(request, "El co-coordinador fue asignado con éxito")

        context = {
            'sesion': co_coordinador_sesion.sesion,
            'cargo': "co-coordinador",
            'arbitraje': sesion.sistema,
        }
        msg_plain = render_to_string('../templates/email_templates/coordinator_assign.txt', context)
        msg_html = render_to_string('../templates/email_templates/coordinator_assign.html', context)

        send_mail(
                'Asignación como co-coordinador',         #titulo
                msg_plain,                          #mensaje txt
                config('EMAIL_HOST_USER'),          #email de envio
                [co_coordinador_sesion.autor.correo_electronico],               #destinatario
                html_message=msg_html,              #mensaje en html
                )

        return redirect('sesiones:sesions_list')

    context = {
        'sesion': sesion,
        'autor': autor
    }
    data['html_form'] = render_to_string('ajax/sesiones_assign_co_coordinator.html',context,request=request)
    return JsonResponse(data)