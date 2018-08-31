# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.urls import reverse
from main_app.models import Rol,Sistema_asovac,Usuario_asovac

from main_app.views import get_route_resultados, get_route_trabajos_navbar, verify_trabajo_options, get_route_trabajos_sidebar, verify_asignar_sesion, get_roles, verify_configuration, verify_arbitration,verify_result,verify_event,validate_rol_status,verify_configuracion_general_option,verify_datos_basicos_option,verify_estado_arbitrajes_option,verify_usuario_option,verify_asignacion_coordinador_general_option,verify_asignacion_coordinador_area_option,verify_recursos_option,verify_areas_subareas_option,verify_autores_option,verify_arbitros_option,verify_sesions_arbitraje_option,verify_arbitraje_option,verify_trabajo_option,verify_eventos_sidebar_full,verify_espacio_option,validate_rol_status,get_route_configuracion,get_route_seguimiento, verify_jobs
from eventos.forms import CreateOrganizerForm,CreateEventForm
from eventos.models import Organizador,Organizador_evento,Evento,Locacion_evento

from main_app.models import Usuario_asovac,Sistema_asovac,Rol

# Create your views here.
def event_list(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Eventos',  'icon': 'fa-archive',   'active': True}]

    secondary_navbar_options = ['']

    context = {
        'nombre_vista' : 'Eventos',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
    }
    return render(request, 'eventos_event_list.html', context)


def event_edit(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Eventos',  'icon': 'fa-archive',   'active': True}]

    secondary_navbar_options = ['']

    rol_id=get_roles(request.user.id)


    context = {
        'nombre_vista' : 'Autores',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
    }
    return render(request, 'eventos_event_edit.html', context)

def event_create(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Eventos',  'icon': 'fa-archive',   'active': True}]

    secondary_navbar_options = ['']

    form = CreateEventForm()
    context = {
        'username' : request.user.username,
        'form' : form,
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
    }
    if request.method == 'POST':
        form = CreateOrganizerForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False)
            #Limpiando la data
            nombre = form.cleaned_data['nombre']
            categoria = form.cleaned_data['categoria']
            descripcion = form.cleaned_data['descripcion']
            tipo = form.cleaned_data['tipo']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            print(fecha_inicio)
            fecha_fin = form.cleaned_data['fecha_fin']
            print(fecha_fin)
            dia_asignado = form.cleaned_data['dia_asignado']
            duracion = form.cleaned_data['duracion']
            horario_preferido = form.cleaned_data['horario_preferido']
            fecha_preferida = form.cleaned_data['fecha_preferida']
            print(fecha_preferida)
            observaciones = form.cleaned_data['observaciones']
            url_anuncio_evento = form.cleaned_data['url_anuncio_evento']
            organizador_id = form.cleaned_data['organizador_id']
            print(type(organizador_id))
            print(organizador_id)
            locacion_evento = form.cleaned_data['locacion_evento']
            print(type(locacion_evento))
            print(locacion_evento)           
            #print(form)
            organizer_data = Organizador.objects.all()
            context = {        
                'username' : request.user.username,
                'form' : form,
                'org_data': organizer_data,
                'main_navbar_options' : main_navbar_options,
                'secondary_navbar_options' : secondary_navbar_options,
                #'verify_event_app' : verify_event_app(),
                }
            return render(request, 'eventos_event_create.html', context) 

    return render(request, 'eventos_event_create.html', context)

def event_delete(request):
    
    return render(request, 'eventos_event_delete.html',context={})

def event_detail(request):
    
    return render(request, 'eventos_event_detail.html',context={})  

def organizer_create(request):
    form = CreateOrganizerForm()
    #print(request.user.id)
    #print(request.user.username)
    user_data = Usuario_asovac.objects.get(pk=request.user.id)
    print(user_data.Sistema_asovac_id.values())
    #user_asov.save()
    # arbitraje al cual pertenece el usuario
    #arbitraje = Sistema_asovac.objects.filter().only(id)
    #print(arbitraje)

    context = {
        'username' : request.user.username,
        'form' : form,
    }
    if request.method == 'POST':
        form = CreateOrganizerForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False)
            #lIMPIANDO DATA
            form.nombres = form.clean_names()
            apellidos = form.clean_lastnames()
            genero = form.clean_gender()

            print(genero)
            cedula_o_pasaporte = form.clean_cedula_pass()
            correo_electronico = form.clean_email()
            institucion = form.clean_institution()
            telefono_oficina = form.clean_phone_office()
            telefono_habitacion_celular = form.clean_phone_personal()
            direccion_correspondencia = form.clean_address()
            es_miembro_asovac = form.clean_asovac_menber()
            print(es_miembro_asovac)
            capitulo_asovac = form.clean_cap_asovac()
            cargo_en_institucion = form.clean_position_institution()
            url_organizador = form.clean_url_organizer()
            observaciones = form.clean_observations()
            usuario_asovac = form.clean_user_asovac()   
            print(usuario_asovac)

            print("El form es valido y se guardo satisfactoriamente")
            organizer_data = Organizador.objects.all()
            context = {        
                'username' : request.user.username,
                'form' : form,
                'org_data': organizer_data,
                #'verify_event_app' : verify_event_app(),
                }
            return redirect(reverse('eventos:organizer_list'), context) 
    return render(request, 'eventos_organizer_create.html',context)

def organizer_list(request):

    return render(request, 'eventos_organizer_list.html', context={})

def organizer_edit(request):

    return render(request, 'eventos_organizer_edit.html', context={})

def organizer_delete(request):

    return render(request, 'eventos_organizer_delete.html',context={})

def organizer_detail(request):
    
    return render(request, 'eventos_organizer_detail.html',context={})