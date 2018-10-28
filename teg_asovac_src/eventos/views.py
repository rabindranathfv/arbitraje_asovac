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

    if request.method == 'POST':
        form = CreateOrganizerForm(request.POST)
        if form.is_valid():
            organizador = form.save(commit=False)
            user = request.user
            usuario_asovac = get_object_or_404(Usuario_asovac,usuario = user)
            organizador.usuario_asovac = usuario_asovac
            organizador.save()
            return redirect(reverse('eventos:organizer_list')) 
    
    context = {
        'username' : request.user.username,
        'form' : form,
    }
    
    return render(request, 'eventos_organizer_create.html',context)


def organizer_list(request):
    organizer_data = Organizador.objects.all().order_by('-id')
    usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
    context = {        
                'username' : request.user.username,
                'organizer_data': organizer_data,
                'usuario_asovac':usuario_asovac,
                }
    return render(request, 'eventos_organizer_list.html', context)


def organizer_edit(request, organizador_id):
    organizador = get_object_or_404(Organizador,id = organizador_id)
    if request.method == 'POST':
        form = CreateOrganizerForm(request.POST, instance = organizador)
        if form.is_valid():
            form.save()
            return redirect(reverse('eventos:organizer_list'))

    form = CreateOrganizerForm(instance = organizador)   
    context = {
        'nombre_vista' : 'Autores',
        'username': request.user.username,
        'form':form
        }
    return render(request, 'eventos_organizer_edit.html', context)


def organizer_delete(request, organizador_id):
    data = dict()
    organizador= get_object_or_404(Organizador, id = organizador_id)
    if request.method == "POST":
        organizador.delete()
        return redirect(reverse('eventos:organizer_list')) 
    else:
        context = {
            'organizador':organizador,
        }
        data['html_form'] = render_to_string('ajax/organizer_delete.html',context,request=request)
    return JsonResponse(data)



def organizer_detail(request, organizador_id):
    data = dict()
    organizador= get_object_or_404(Organizador, id = organizador_id)
    context = {
            'organizador':organizador,
        }
    data['html_form'] = render_to_string('ajax/organizer_details.html',context,request=request)
    return JsonResponse(data)


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

def event_place_edit(request, locacion_id):
    locacion = get_object_or_404(Locacion_evento,id = locacion_id)
    if request.method == 'POST':
        form = CreateLocacionForm(request.POST, instance = locacion)
        if form.is_valid():
            form.save()
            return redirect(reverse('eventos:event_place_list'))

    form = CreateLocacionForm(instance = locacion)   
    context = {
        'nombre_vista' : 'Autores',
        'username': request.user.username,
        'form':form
        }
    return render(request, 'eventos_locacion_edit.html', context)

def event_place_delete(request, locacion_id):
    data = dict()
    locacion = get_object_or_404(Locacion_evento, id = locacion_id)
    if request.method == "POST":
        locacion.delete()
        return redirect(reverse('eventos:event_place_list')) 
    else:
        context = {
            'locacion':locacion,
        }
        data['html_form'] = render_to_string('ajax/location_delete.html',context,request=request)
    return JsonResponse(data)


def event_place_detail(request, locacion_id):
    locacion = get_object_or_404(Locacion_evento, id = locacion_id)
    
    context = {
        'nombre_vista' : 'Autores',
        'username': request.user.username,
        'locacion': locacion,
    }
    return render(request, 'eventos_locacion_details.html', context)