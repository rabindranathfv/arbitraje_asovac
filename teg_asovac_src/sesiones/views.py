# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from main_app.models import Rol,Sistema_asovac,Usuario_asovac

# Create your views here.
def sesiones_pag(request):
    context = {
        "nombre_vista": 'sesiones'
    }
    return render(request,"test_views.html",context)

def sesions_list(request):
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

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'item_active' : '2',
        'username' : 'Username',
    }
    return render(request, 'sesiones_sesions_list.html', context)

def sesions_edit(request):
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

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'item_active' : '2',
        'username' : 'Username',
    }
    return render(request, 'sesiones_sesions_edit.html', context)

def sesions_space_list(request):
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

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'event_id' : event_id,
        'rol' : rol,
        'rol_id' : rol_id,
        'item_active' : '2',
        'username' : 'Username',
    }
    return render(request, 'sesiones_space_list.html', context)

def sesions_space_edit(request):
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

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'event_id' : event_id,
        'rol' : rol,
        'rol_id' : rol_id,
        'item_active' : '2',
        'username' : 'Username',
    }
    return render(request, 'sesiones_space_edit.html', context)