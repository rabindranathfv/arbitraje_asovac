# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, validate_rol_status ,validate_rol_status,get_route_configuracion,get_route_seguimiento

#Import forms
from eventos.forms import CreateOrganizerForm,CreateEventForm,CreateLocacionForm, EditEventForm

#Import Models
from eventos.models import Organizador,Organizador_evento,Evento,Locacion_evento
from .models import Organizador,Organizador_evento,Evento,Locacion_evento
from main_app.models import Usuario_asovac,Sistema_asovac,Rol

# Create your views here.
def event_create(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            evento = form.save()
            locacion_preferida = form.cleaned_data['locacion_preferida']
            
            user = request.user
            usuario_asovac = Usuario_asovac.objects.get(usuario = user)
            organizador = Organizador.objects.get(usuario_asovac = usuario_asovac)
            organizador_evento = Organizador_evento(organizador = organizador, evento = evento, locacion_preferida = locacion_preferida)
            organizador_evento.save()
            """
            organizador_email_list = form.cleaned_data['organizador_id']
            for organizador_email in organizador_email_list:
                organizador = Organizador.objects.get(correo_electronico = organizador_email)
                organizador_evento = Organizador_evento(organizador = organizador, evento = evento, locacion_preferida = locacion_preferida)
                organizador_evento.save()
            """
            print("El form es valido y se guardo satisfactoriamente el EVENTO")
            return redirect(reverse('eventos:event_list')) 
    else:
        form = CreateEventForm()
    context = {
        'username' : request.user.username,
        'form' : form,
    }
    return render(request, 'eventos_event_create.html',context)


def event_list(request):
    event_data = Evento.objects.all().order_by('-id')
    #for data in event_data:
        #print("nombre " + data.nombre)
    context = {
        'nombre_vista' : 'Eventos',
        'username': request.user.username,
        'event_data': event_data,
    }
    return render(request, 'eventos_event_list.html', context)


def event_edit(request, evento_id):
    evento = get_object_or_404(Evento,id = evento_id)
    if request.method == 'POST':
        form = EditEventForm(request.POST, instance = evento)
        if form.is_valid():
            form.save()
            return redirect(reverse('eventos:event_list'))

    form = EditEventForm(instance = evento)   
    context = {
        'nombre_vista' : 'Autores',
        'username': request.user.username,
        'form':form
        }
    return render(request, 'eventos_event_edit.html', context)


def event_delete(request, evento_id):
    data = dict()
    evento = get_object_or_404(Evento, id = evento_id)
    if request.method == "POST":
        evento.delete()
        return redirect(reverse('eventos:event_list')) 
    else:
        context = {
            'evento':evento,
        }
        data['html_form'] = render_to_string('ajax/event_delete.html',context,request=request)
    return JsonResponse(data)


def event_detail(request, evento_id):
    evento = get_object_or_404(Evento, id = evento_id)
    
    context = {
        'nombre_vista' : 'Autores',
        'username': request.user.username,
        'evento': evento,
    }
    return render(request, 'eventos_event_detail.html',context)  

##################### Organizer Views ###########################

def organizer_create(request):
    form = CreateOrganizerForm()

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
            form.apellidos = form.clean_lastnames()
            form.genero = form.clean_gender()

            #print(form.genero)
            form.cedula_o_pasaporte = form.clean_cedula_pass()
            form.correo_electronico = form.clean_email()
            form.institucion = form.clean_institution()
            form.telefono_oficina = form.clean_phone_office()
            form.telefono_habitacion_celular = form.clean_phone_personal()
            form.direccion_correspondencia = form.clean_address()
            form.es_miembro_asovac = form.clean_asovac_menber()
            #print(form.es_miembro_asovac)
            form.capitulo_asovac = form.clean_cap_asovac()
            form.cargo_en_institucion = form.clean_position_institution()
            form.url_organizador = form.clean_url_organizer()
            form.observaciones = form.clean_observations()
            form.usuario_asovac = form.clean_user_asovac()   
            #print(form.usuario_asovac)

            print("El form es valido y se guardo satisfactoriamente")
            form.save()
            return redirect(reverse('eventos:organizer_list')) 
    return render(request, 'eventos_organizer_create.html',context)

def organizer_list(request):
    organizer_data = Organizador.objects.all().order_by('-id')
    context = {        
                'username' : request.user.username,
                'organizer_data': organizer_data,
                }
    return render(request, 'eventos_organizer_list.html', context)

def organizer_edit(request):

    return render(request, 'eventos_organizer_edit.html', context={})

def organizer_delete(request):

    return render(request, 'eventos_organizer_delete.html',context={})

def organizer_detail(request):
    
    return render(request, 'eventos_organizer_detail.html',context={})

##################### Locacion Views ###########################

def event_place_create(request):
    

    if request.method == 'POST':
        form = CreateLocacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('eventos:event_place_list'))
    form = CreateLocacionForm()
    context = {
        'nombre_vista' : 'Crear locación de evento',
        'username': request.user.username,
        'form': form,
    }
    return render(request, 'eventos_locacion_create.html', context)

def event_place_list(request):
    event_place_data = Locacion_evento.objects.all().order_by('id')
    context = {        
                'username' : request.user.username,
                'event_place_data': event_place_data,
                }
    return render(request, 'eventos_locacion_list.html', context)

def event_place_edit(request):
    
    return render(request, 'eventos_locacion_edit.html', context={})

def event_place_delete(request):
    
    return render(request, 'eventos_locacion_delete.html', context={})

def event_place_detail(request):
    
    return render(request, 'eventos_locacion_detail.html', context={})