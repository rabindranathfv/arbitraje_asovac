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

from main_app.models import Rol,Sistema_asovac,Usuario_asovac

# Global functions
# Esta función verifica que se va a desplegar la opción de configuracion general en el sidebar, retorna 1 si se usará y 0 sino.
def verify_configuracion_general_option(estado, rol_id, item_active): 
    if ((estado == '0' or estado =='1' or estado =='3' or estado =='5' or estado =='6' or estado =='7' or estado == '8') and 1 in rol_id and item_active == 1) or ((estado =='2' or estado == '4') and (1 in rol_id or 2 in rol_id) and item_active == 1):
        return 1
    return 0

def verify_datos_basicos_option(estado,rol_id,item_active):
    if(estado == '2' and (1 not in rol_id and 2 not in rol_id) and item_active == 1) or (estado == '4' and (1 not in rol_id and 2 not in rol_id) and item_active ==1):
        return 0
    return 1

def verify_estado_arbitrajes_option(estado,rol_id,item_active):
    if(estado == '4' and 2 in rol_id and item_active == 1):
        return 0
    return 1


def verify_usuario_option(estado,rol_id, item_active):
    if ((estado == '0' or estado =='1' or estado =='2' or estado == '3' or estado == '4' or estado == '5' or estado == '6' or estado =='7' or estado =='8') and 1 in rol_id and item_active == 1):
        return 1
    return 0


def verify_asignacion_coordinador_general_option(estado,rol_id,item_active):
    if((estado == '1' or estado =='2' or estado == '3' or estado == '4' or estado == '5' or estado =='6' or estado =='7' or estado =='8') and  1 in rol_id and item_active == 1):
        return 1
    return 0


def verify_asignacion_coordinador_area_option(estado,rol_id,item_active):
    if(estado =='2' and  (1 in rol_id or 2 in rol_id) and item_active ==1) or((estado == '3' or estado == '4' or estado == '5' or estado =='6' or estado =='7' or estado =='8') and 1 in rol_id and item_active == 1):
        return 1
    return 0




def verify_recursos_option(estado,rol_id,item_active):
    if ((estado == '0' or estado == '1' or estado == '2' or estado == '3' or estado == '4' or estado == '5' or estado =='6' or estado =='7') and 1 in rol_id and item_active == 1) or (estado =='8' and (1 in rol_id or 2 in rol_id or 3 in rol_id) and item_active==1):
        return 1
    return 0

def verify_areas_subareas_option(estado,rol_id,item_active):
    if ((estado == '0' or estado =='3' or estado == '4' or estado == '5' or estado =='6' or estado =='7' or estado =='8') and 1 in rol_id and item_active == 1) or (estado == '1' and (1 in rol_id or 2 in rol_id or 3 in rol_id) and item_active == 1) or (estado == '2' and (1 in rol_id or 2 in rol_id) and item_active ==1):
        return 1
    return 0


def verify_autores_option(estado,rol_id,item_active):
    if ((estado == '0' or estado =='5' or estado =='6' or estado =='7' or estado =='8') and 1 in rol_id and item_active == 2) or ((estado == '1' or estado =='2' or estado == '3' or estado == '4') and (1 in rol_id or 2 in rol_id) and item_active == 2):
        return 1
    return 0

def verify_arbitros_option(estado,rol_id, item_active):
    if ((estado == '0' or estado =='5' or estado =='6' or estado =='7' or estado =='8') and 1 in rol_id and item_active == 2) or ((estado == '1' or estado =='2' or estado == '3' or estado == '4') and (1 in rol_id or 2 in rol_id or 3 in rol_id) and item_active == 2):
        return 1
    return 0

def verify_sesions_arbitraje_option(estado,rol_id, item_active):
    if ((estado == '0' or estado =='1' or estado == '2' or estado == '3' or estado =='5' or estado =='6' or estado =='8') and 1 in rol_id and item_active == 2) or ((estado == '4' or estado =='7') and (1 in rol_id or 2 in rol_id or 3 in rol_id) and item_active == 2):
        return 1
    return 0

def verify_arbitraje_option(estado,rol_id, item_active):
    if ((estado == '0' or estado =='1' or estado == '2' or estado == '3' or estado == '4' or estado =='5' or estado =='7' or estado =='8') and 1 in rol_id and item_active == 2) or (estado =='6' and (1 in rol_id or 2 in rol_id or 3 in rol_id) and item_active == 2):
        return 1
    return 0

def verify_trabajo_option(estado, rol_id,item_active):
    if((estado =='3' or estado =='4' or estado =='5')and (1 in rol_id or 2 in rol_id or 3 in rol_id) and item_active == 2) or ((estado =='6' or estado =='7' or estado =='8') and 1 in rol_id and item_active ==2):
        return 1
    return 0

def verify_eventos_sidebar_full(estado,rol_id,item_active):
    if ((estado == '0' or estado =='1' or estado == '2' or estado == '3' or estado == '4' or estado =='5' or estado =='6' or estado =='7' or estado =='8') and 1 in rol_id and item_active == 4):
        return 1
    return 0

def verify_espacio_option(estado,rol_id,item_active):
    if((estado =='7' or estado =='8') and 1 in rol_id and item_active == 4):
        return 1
    return 0


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

    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all() 

    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    print (rol_id)

    item_active = 1
    configuracion_general_sidebar = verify_configuracion_general_option(estado, rol_id, item_active)
    usuarios_sidebar = verify_usuario_option(estado,rol_id,item_active)
    recursos_sidebar = verify_recursos_option(estado,rol_id,item_active)
    areas_subareas_sidebar = verify_areas_subareas_option(estado,rol_id,item_active)

    autores_sidebar = verify_autores_option(estado,rol_id,item_active)
    arbitros_sidebar = verify_arbitros_option(estado,rol_id,item_active)
    sesion_arbitraje_sidebar = verify_sesions_arbitraje_option(estado,rol_id,item_active)
    arbitraje_sidebar = verify_arbitraje_option(estado,rol_id,item_active)
    eventos_sidebar_full = verify_eventos_sidebar_full(estado,rol_id,item_active)

    asignacion_coordinador_general = verify_asignacion_coordinador_general_option(estado,rol_id,item_active)

    asignacion_coordinador_area = verify_asignacion_coordinador_area_option(estado, rol_id,item_active)
    datos_basicos_sidebar = verify_datos_basicos_option(estado,rol_id,item_active)

    trabajos_sidebar = verify_trabajo_option(estado,rol_id,item_active)

    estado_arbitrajes_sidebar = verify_estado_arbitrajes_option(estado,rol_id,item_active)

    espacio_sidebar = verify_espacio_option(estado,rol_id,item_active)
    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
        'configuracion_general_sidebar': configuracion_general_sidebar,
        'usuarios_sidebar' : usuarios_sidebar,
        'recursos_sidebar' : recursos_sidebar,
        'areas_subareas_sidebar' : areas_subareas_sidebar,
        'autores_sidebar' : autores_sidebar,
        'arbitros_sidebar' : arbitros_sidebar,
        'sesion_arbitraje_sidebar' : sesion_arbitraje_sidebar,
        'arbitraje_sidebar' : arbitraje_sidebar,
        'eventos_sidebar_full' : eventos_sidebar_full,
        'asignacion_coordinador_general': asignacion_coordinador_general,
        'asignacion_coordinador_area': asignacion_coordinador_area,
        'datos_basicos_sidebar' : datos_basicos_sidebar,
        'trabajos_sidebar':trabajos_sidebar,
        'estado_arbitrajes_sidebar':estado_arbitrajes_sidebar,
        'espacio_sidebar':espacio_sidebar,
    }
    return render(request, 'main_app_resources_author.html', context)

def resources_referee(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()

    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    print (rol_id)

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=-1
        event_id=-1

    item_active = 1
    configuracion_general_sidebar = verify_configuracion_general_option(estado, rol_id, item_active)
    usuarios_sidebar = verify_usuario_option(estado,rol_id,item_active)
    recursos_sidebar = verify_recursos_option(estado,rol_id,item_active)
    areas_subareas_sidebar = verify_areas_subareas_option(estado,rol_id,item_active)

    autores_sidebar = verify_autores_option(estado,rol_id,item_active)
    arbitros_sidebar = verify_arbitros_option(estado,rol_id,item_active)
    sesion_arbitraje_sidebar = verify_sesions_arbitraje_option(estado,rol_id,item_active)
    arbitraje_sidebar = verify_arbitraje_option(estado,rol_id,item_active)
    eventos_sidebar_full = verify_eventos_sidebar_full(estado,rol_id,item_active)

    asignacion_coordinador_general = verify_asignacion_coordinador_general_option(estado,rol_id,item_active)

    asignacion_coordinador_area = verify_asignacion_coordinador_area_option(estado, rol_id,item_active)
    datos_basicos_sidebar = verify_datos_basicos_option(estado,rol_id,item_active)

    trabajos_sidebar = verify_trabajo_option(estado,rol_id,item_active)

    estado_arbitrajes_sidebar = verify_estado_arbitrajes_option(estado,rol_id,item_active)

    espacio_sidebar = verify_espacio_option(estado,rol_id,item_active)
    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'item_active' : '1',
        'username' : 'Username',
        'configuracion_general_sidebar': configuracion_general_sidebar,
        'usuarios_sidebar' : usuarios_sidebar,
        'recursos_sidebar' : recursos_sidebar,
        'areas_subareas_sidebar' : areas_subareas_sidebar,
        'autores_sidebar' : autores_sidebar,
        'arbitros_sidebar' : arbitros_sidebar,
        'sesion_arbitraje_sidebar' : sesion_arbitraje_sidebar,
        'arbitraje_sidebar' : arbitraje_sidebar,
        'eventos_sidebar_full' : eventos_sidebar_full,
        'asignacion_coordinador_general': asignacion_coordinador_general,
        'asignacion_coordinador_area': asignacion_coordinador_area,
        'datos_basicos_sidebar' : datos_basicos_sidebar,
        'trabajos_sidebar':trabajos_sidebar,
        'estado_arbitrajes_sidebar':estado_arbitrajes_sidebar,
        'espacio_sidebar':espacio_sidebar,
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

    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()

    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    item_active = 1
    configuracion_general_sidebar = verify_configuracion_general_option(estado, rol_id, item_active)
    usuarios_sidebar = verify_usuario_option(estado,rol_id,item_active)
    recursos_sidebar = verify_recursos_option(estado,rol_id,item_active)
    areas_subareas_sidebar = verify_areas_subareas_option(estado,rol_id,item_active)

    autores_sidebar = verify_autores_option(estado,rol_id,item_active)
    arbitros_sidebar = verify_arbitros_option(estado,rol_id,item_active)
    sesion_arbitraje_sidebar = verify_sesions_arbitraje_option(estado,rol_id,item_active)
    arbitraje_sidebar = verify_arbitraje_option(estado,rol_id,item_active)
    eventos_sidebar_full = verify_eventos_sidebar_full(estado,rol_id,item_active)

    asignacion_coordinador_general = verify_asignacion_coordinador_general_option(estado,rol_id,item_active)

    asignacion_coordinador_area = verify_asignacion_coordinador_area_option(estado, rol_id,item_active)
    datos_basicos_sidebar = verify_datos_basicos_option(estado,rol_id,item_active)

    trabajos_sidebar = verify_trabajo_option(estado,rol_id,item_active)

    estado_arbitrajes_sidebar = verify_estado_arbitrajes_option(estado,rol_id,item_active)

    espacio_sidebar = verify_espacio_option(estado,rol_id,item_active)
    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
        'configuracion_general_sidebar': configuracion_general_sidebar,
        'usuarios_sidebar' : usuarios_sidebar,
        'recursos_sidebar' : recursos_sidebar,
        'areas_subareas_sidebar' : areas_subareas_sidebar,
        'autores_sidebar' : autores_sidebar,
        'arbitros_sidebar' : arbitros_sidebar,
        'sesion_arbitraje_sidebar' : sesion_arbitraje_sidebar,
        'arbitraje_sidebar' : arbitraje_sidebar,
        'eventos_sidebar_full' : eventos_sidebar_full,
        'asignacion_coordinador_general': asignacion_coordinador_general,
        'asignacion_coordinador_area': asignacion_coordinador_area,
        'datos_basicos_sidebar' : datos_basicos_sidebar,
        'trabajos_sidebar':trabajos_sidebar,
        'estado_arbitrajes_sidebar':estado_arbitrajes_sidebar,
        'espacio_sidebar':espacio_sidebar,
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

    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()

    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    item_active = 1
    configuracion_general_sidebar = verify_configuracion_general_option(estado, rol_id, item_active)
    usuarios_sidebar = verify_usuario_option(estado,rol_id,item_active)
    recursos_sidebar = verify_recursos_option(estado,rol_id,item_active)
    areas_subareas_sidebar = verify_areas_subareas_option(estado,rol_id,item_active)

    autores_sidebar = verify_autores_option(estado,rol_id,item_active)
    arbitros_sidebar = verify_arbitros_option(estado,rol_id,item_active)
    sesion_arbitraje_sidebar = verify_sesions_arbitraje_option(estado,rol_id,item_active)
    arbitraje_sidebar = verify_arbitraje_option(estado,rol_id,item_active)
    eventos_sidebar_full = verify_eventos_sidebar_full(estado,rol_id,item_active)

    asignacion_coordinador_general = verify_asignacion_coordinador_general_option(estado,rol_id,item_active)

    asignacion_coordinador_area = verify_asignacion_coordinador_area_option(estado, rol_id,item_active)
    datos_basicos_sidebar = verify_datos_basicos_option(estado,rol_id,item_active)

    trabajos_sidebar = verify_trabajo_option(estado,rol_id,item_active)

    estado_arbitrajes_sidebar = verify_estado_arbitrajes_option(estado,rol_id,item_active)

    espacio_sidebar = verify_espacio_option(estado,rol_id,item_active)
    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
        'configuracion_general_sidebar': configuracion_general_sidebar,
        'usuarios_sidebar' : usuarios_sidebar,
        'recursos_sidebar' : recursos_sidebar,
        'areas_subareas_sidebar' : areas_subareas_sidebar,
        'autores_sidebar' : autores_sidebar,
        'arbitros_sidebar' : arbitros_sidebar,
        'sesion_arbitraje_sidebar' : sesion_arbitraje_sidebar,
        'arbitraje_sidebar' : arbitraje_sidebar,
        'eventos_sidebar_full' : eventos_sidebar_full,
        'asignacion_coordinador_general': asignacion_coordinador_general,
        'asignacion_coordinador_area': asignacion_coordinador_area,
        'datos_basicos_sidebar' : datos_basicos_sidebar,
        'trabajos_sidebar':trabajos_sidebar,
        'estado_arbitrajes_sidebar':estado_arbitrajes_sidebar,
        'espacio_sidebar':espacio_sidebar,
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

    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()

    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    item_active = 1
    configuracion_general_sidebar = verify_configuracion_general_option(estado, rol_id, item_active)
    usuarios_sidebar = verify_usuario_option(estado,rol_id,item_active)
    recursos_sidebar = verify_recursos_option(estado,rol_id,item_active)
    areas_subareas_sidebar = verify_areas_subareas_option(estado,rol_id,item_active)

    autores_sidebar = verify_autores_option(estado,rol_id,item_active)
    arbitros_sidebar = verify_arbitros_option(estado,rol_id,item_active)
    sesion_arbitraje_sidebar = verify_sesions_arbitraje_option(estado,rol_id,item_active)
    arbitraje_sidebar = verify_arbitraje_option(estado,rol_id,item_active)
    eventos_sidebar_full = verify_eventos_sidebar_full(estado,rol_id,item_active)

    asignacion_coordinador_general = verify_asignacion_coordinador_general_option(estado,rol_id,item_active)

    asignacion_coordinador_area = verify_asignacion_coordinador_area_option(estado, rol_id,item_active)
    datos_basicos_sidebar = verify_datos_basicos_option(estado,rol_id,item_active)

    trabajos_sidebar = verify_trabajo_option(estado,rol_id,item_active)

    estado_arbitrajes_sidebar = verify_estado_arbitrajes_option(estado,rol_id,item_active)

    espacio_sidebar = verify_espacio_option(estado,rol_id,item_active)
    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
        'configuracion_general_sidebar': configuracion_general_sidebar,
        'usuarios_sidebar' : usuarios_sidebar,
        'recursos_sidebar' : recursos_sidebar,
        'areas_subareas_sidebar' : areas_subareas_sidebar,
        'autores_sidebar' : autores_sidebar,
        'arbitros_sidebar' : arbitros_sidebar,
        'sesion_arbitraje_sidebar' : sesion_arbitraje_sidebar,
        'arbitraje_sidebar' : arbitraje_sidebar,
        'eventos_sidebar_full' : eventos_sidebar_full,
        'asignacion_coordinador_general': asignacion_coordinador_general,
        'asignacion_coordinador_area': asignacion_coordinador_area,
        'datos_basicos_sidebar' : datos_basicos_sidebar,
        'trabajos_sidebar':trabajos_sidebar,
        'estado_arbitrajes_sidebar':estado_arbitrajes_sidebar,
        'espacio_sidebar':espacio_sidebar,
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

    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()

    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    item_active = 1
    configuracion_general_sidebar = verify_configuracion_general_option(estado, rol_id, item_active)
    usuarios_sidebar = verify_usuario_option(estado,rol_id,item_active)
    recursos_sidebar = verify_recursos_option(estado,rol_id,item_active)
    areas_subareas_sidebar = verify_areas_subareas_option(estado,rol_id,item_active)

    autores_sidebar = verify_autores_option(estado,rol_id,item_active)
    arbitros_sidebar = verify_arbitros_option(estado,rol_id,item_active)
    sesion_arbitraje_sidebar = verify_sesions_arbitraje_option(estado,rol_id,item_active)
    arbitraje_sidebar = verify_arbitraje_option(estado,rol_id,item_active)
    eventos_sidebar_full = verify_eventos_sidebar_full(estado,rol_id,item_active)

    asignacion_coordinador_general = verify_asignacion_coordinador_general_option(estado,rol_id,item_active)

    asignacion_coordinador_area = verify_asignacion_coordinador_area_option(estado, rol_id,item_active)
    datos_basicos_sidebar = verify_datos_basicos_option(estado,rol_id,item_active)

    trabajos_sidebar = verify_trabajo_option(estado,rol_id,item_active)

    estado_arbitrajes_sidebar = verify_estado_arbitrajes_option(estado,rol_id,item_active)

    espacio_sidebar = verify_espacio_option(estado,rol_id,item_active)
    context = {
        'nombre_vista' : 'Arbitros',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : '1',
        'username' : 'Username',
        'configuracion_general_sidebar': configuracion_general_sidebar,
        'usuarios_sidebar' : usuarios_sidebar,
        'recursos_sidebar' : recursos_sidebar,
        'areas_subareas_sidebar' : areas_subareas_sidebar,
        'autores_sidebar' : autores_sidebar,
        'arbitros_sidebar' : arbitros_sidebar,
        'sesion_arbitraje_sidebar' : sesion_arbitraje_sidebar,
        'arbitraje_sidebar' : arbitraje_sidebar,
        'eventos_sidebar_full' : eventos_sidebar_full,
        'asignacion_coordinador_general': asignacion_coordinador_general,
        'asignacion_coordinador_area': asignacion_coordinador_area,
        'datos_basicos_sidebar' : datos_basicos_sidebar,
        'trabajos_sidebar':trabajos_sidebar,
        'estado_arbitrajes_sidebar':estado_arbitrajes_sidebar,
        'espacio_sidebar':espacio_sidebar,

    }
    return render(request, 'main_app_resources_arbitrations.html', context)

