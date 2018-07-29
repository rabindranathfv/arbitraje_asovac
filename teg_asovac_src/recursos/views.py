# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect

#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from django.http import HttpResponse

# import funcion in utils.py
from .utils import render_to_pdf
# for load template to render to pdf
from django.template.loader import get_template

# Create your views here.
def recursos_pag(request):
    context = {
        "nombre_vista": 'recursos'
    }
    return render(request,"test_views.html",context)

def generate_pdf(request,*args , **kwargs):
    #obtener el template
    template = get_template('pdf/modelo_pdf.html')
    # hacer querysets
    
    # Data a renderizar en el template
    context = {}
    # render template
    html = template.render(context)
    # to download in pdf
    pdf = render_to_pdf('pdf/modelo_pdf.html',context)
    #respuesta del pdf en el navegador
    if pdf:
        return HttpResponse(pdf, content_type='application/pdf')
    return HttpResponse("Crear pagina de Error 404")

def resources_author(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=-1
        event_id=-1

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_author.html', context)

def resources_referee(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=-1
        event_id=-1

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_referee.html', context)

def resources_event(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=-1
        event_id=-1

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_event.html', context)

def resources_sesion(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=-1
        event_id=-1

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_sesion.html', context)

def resources_asovac(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=-1
        event_id=-1

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_asovac.html', context)

def resources_arbitration(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=-1
        event_id=-1

    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_resources_arbitrations.html', context)

