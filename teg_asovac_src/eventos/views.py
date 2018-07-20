# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def eventos_pag(request):
    context = {
        "nombre_vista": 'Recursos'
    }
    return render(request,"test_views.html",context)

def event_list(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'username' : 'Username',
    }
    return render(request, 'main_app_event_list.html', context)