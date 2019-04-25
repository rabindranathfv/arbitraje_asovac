# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .models import Sesion, Coordinadores_sesion, Espacio
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

# Create your views here.
def sesiones_pag(request):
    context = {
        "nombre_vista": 'sesiones'
    }
    return render(request,"test_views.html",context)

####################### Inclusión de eventos en arbitrajes########################
def sesions_list(request):
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
        data=Coordinadores_sesion.objects.filter( Q(sesion__sistema = arbitraje_id) & (Q(sesion__espacio__espacio_virtual__url_virtual__icontains = search) | Q(sesion__espacio__espacio_fisico__nombre__icontains = search) | Q(sesion__sistema = arbitraje_id) & (Q(sesion__nombre_sesion__icontains=search) | Q(sesion__fecha_sesion__icontains=search) | Q(sesion__modalidad__icontains = search) | Q(autor__nombres__icontains = search) | Q(autor__apellidos__icontains = search)))).order_by(order)[init:limit]
        total=Coordinadores_sesion.objects.filter( Q(sesion__sistema = arbitraje_id) & (Q(sesion__espacio__espacio_virtual__url_virtual__icontains = search) | Q(sesion__espacio__espacio_fisico__nombre__icontains = search) |Q(sesion__nombre_sesion__icontains=search) | Q(sesion__fecha_sesion__icontains=search) | Q(sesion__modalidad__icontains = search) | Q(autor__nombres__icontains = search) | Q(autor__apellidos__icontains = search))).distinct('sesion').count()
        
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
                    coordinador = autor.nombres + ' ' + autor.apellidos
                if coordinador_sesion.co_coordinador == True:
                    co_coordinador = autor.nombres + ' ' + autor.apellidos

            #Condicional para obtener el lugar de presentación
            if item.sesion.espacio.espacio_fisico:
                lugar = item.sesion.espacio.espacio_fisico.nombre
            else:
                lugar = item.sesion.espacio.espacio_virtual.url_virtual

            if Trabajo.objects.filter(sesion = item.sesion).exists():
                eliminar = False
            else:
                eliminar = True
            print eliminar
            response['query'].append({'sesion__id':item.sesion.id, 'sesion__nombre_sesion': item.sesion.nombre_sesion, 'sesion__modalidad': item.sesion.modalidad, 'sesion__fecha_sesion': item.sesion.fecha_sesion.strftime("%Y-%m-%d"), 'sesion__hora_sesion': item.sesion.fecha_sesion.strftime("%I:%M %p"), 'autor': coordinador, 'autor_2': co_coordinador, 'lugar': lugar, 'eliminar': eliminar  })
            listed.append(item.sesion.id)

    response={
        'total': total,
        'query': response,
    }

    return JsonResponse(response)




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
            
            messages.success(request, "Sesion creada con éxito.")
            return redirect('sesiones:sesions_list')
        print modalidad
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


def delete_sesion(request, sesion_id):
    
    data = dict()
    sesion = get_object_or_404(Sesion, id = sesion_id)
    if request.method == "POST":
        espacio = sesion.espacio
        if espacio.espacio_fisico:
            lugar = espacio.espacio_fisico
        else:
            lugar = espacio.espacio_virtual
        sesion.delete()
        espacio.delete()
        lugar.delete()
        messages.success(request, "Sesión eliminada con éxito")
        return redirect('sesiones:sesions_list') 
    else:
        context = {
            'sesion':sesion,
        }
        data['html_form'] = render_to_string('ajax/sesion_delete.html',context,request=request)
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
    if sesion.espacio.espacio_fisico:    
        virtual_selected = False
    else:
        virtual_selected = True
    print sesion
    if request.method == 'POST': 
        pass
    else:
        sesion_form = SesionForm(instance = sesion, initial = {'fecha_ocupacion': sesion.espacio.fecha_ocupacion})
        espacio_form = EspacioFisicoForm(instance = sesion.espacio.espacio_fisico )
    
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
        'espacio_form': espacio_form,
        'virtual_selected': virtual_selected
    }
    return render(request,"sesiones_create_sesion.html",context)