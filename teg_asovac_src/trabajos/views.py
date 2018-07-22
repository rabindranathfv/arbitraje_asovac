# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from .forms import TrabajoForm

def trabajos(request):
    form = TrabajoForm()
    context = {
        "nombre_vista": 'Autores',
        "form": form,
    }
    return render(request,"trabajos.html",context)

def jobs_list(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'username' : 'Username',
    }
    return render(request, 'trabajos_jobs_list.html', context)

def jobs_edit(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'username' : 'Username',
    }
    return render(request, 'trabajos_jobs_edit.html', context)
   

def edit_trabajo(request):
	form = TrabajoForm()
	context = {
		"nombre_vista": 'Editar Trabajo',
		"form": form,
    }
	return render(request,"trabajos_edit_trabajo.html",context)

def trabajos_evaluados(request):
	context = {
		"nombre_vista": 'Trabajos Evaluados'
	}
	return render(request,"trabajos_trabajos_evaluados.html",context)

