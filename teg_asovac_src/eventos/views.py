# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from main_app.models import Rol,Sistema_asovac,Usuario_asovac
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status

from .forms import CreateOrganizerForm
from .models import Organizador,Organizador_evento,Evento,Locacion_evento

# Create your views here.
def event_list(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Eventos',  'icon': 'fa-archive',   'active': True}]

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
        # 'estado' : estado,
        # 'rol_id' : rol_id,
        # 'arbitraje_id' : arbitraje_id,
        # 'item_active' : item_active,
        # 'items':items,
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
        # 'estado' : estado,
        # 'rol_id' : rol_id,
        # 'arbitraje_id' : arbitraje_id,
        # 'item_active' : item_active,
        # 'items':items,
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


    context = {
        'nombre_vista' : 'Eventos',
        'main_navbar_options' : main_navbar_options,
        # 'estado' : estado,
        # 'rol_id' : rol_id,
        # 'arbitraje_id' : arbitraje_id,
        # 'item_active' : item_active,
        # 'items':items,
        # 'route_conf':route_conf,
        # 'route_seg':route_seg,
        # 'route_trabajos_sidebar':route_trabajos_sidebar,
        # 'route_trabajos_navbar': route_trabajos_navbar,
        # 'route_resultados': route_resultados,
    }
    return render(request, 'eventos_event_create.html', context)

def organizer_create(request):
    form = CreateOrganizerForm()
    context = {
        'username' : request.user.username,
        'form' : form,
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