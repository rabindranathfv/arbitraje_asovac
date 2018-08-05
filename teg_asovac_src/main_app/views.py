# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .forms import MyLoginForm, CreateArbitrajeForm, RegisterForm, DataBasicForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.urls import reverse
from .models import Rol,Sistema_asovac,Usuario_asovac

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

# Funciones para verificar los campos del navbar
def verify_configuration(estado,rol_id):
    if ( ((estado =='0' or estado == '3' or estado == '5' or estado == '6' or estado=='7' ) and 2 in rol_id) or ((estado != '1' and estado != '8') and 3 in rol_id) or ((estado != '8') and 4 in rol_id)):
        return 0 
    return 1

def verify_arbitration(estado,rol_id):
    if ( ((estado =='0' or estado == '8') and 2 in rol_id) or ((estado == '0' and estado == '8') and 3 in rol_id) or ((estado != '5' or estado != '6') and 4 in rol_id)):
        return 0 
    return 1

def verify_result(estado,rol_id):
    if ( ((estado !='6' and estado != '8') and 2 in rol_id) or ((estado != '6' and estado != '8') and 3 in rol_id) or ((estado != '8' and estado != '6') and 4 in rol_id)):
        return 0 
    return 1

def verify_event(estado,rol_id):
    if (  1 not in rol_id):
        return 0 
    return 1

def validate_rol_status(estado,rol_id,item_active):
    items={}
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

    configuration= verify_configuration(estado,rol_id)
    arbitration= verify_arbitration(estado,rol_id)
    result=  verify_result(estado,rol_id)
    event= verify_event(estado,rol_id)

    # Menu de configuración 
    items.setdefault("configuracion_general_sidebar",[configuracion_general_sidebar,reverse('main_app:data_basic')])
    items.setdefault("usuarios_sidebar",[usuarios_sidebar,reverse('main_app:users_list')])
    items.setdefault("recursos_sidebar",[recursos_sidebar,reverse('recursos:resources_author')])
    items.setdefault("areas_subareas_sidebar",[areas_subareas_sidebar,reverse('arbitrajes:arbitrations_areas_subareas')])
    items.setdefault("estado_arbitrajes_sidebar",[estado_arbitrajes_sidebar,reverse('main_app:arbitration_state')])
    items.setdefault("datos_basicos_sidebar",[datos_basicos_sidebar,reverse('main_app:data_basic')])
    items.setdefault("asignacion_coordinador_general",[asignacion_coordinador_general,reverse('main_app:coord_general')])
    items.setdefault("asignacion_coordinador_area",[asignacion_coordinador_area,reverse('main_app:coord_area')])

    # Menu de arbitraje y seguimiento
    items.setdefault("autores_sidebar",[autores_sidebar,reverse('autores:authors_list')])
    items.setdefault("arbitros_sidebar",[arbitros_sidebar,reverse('arbitrajes:referee_list')])
    items.setdefault("sesion_arbitraje_sidebar",[sesion_arbitraje_sidebar,reverse('sesiones:sesions_list')])
    items.setdefault("arbitraje_sidebar",[arbitraje_sidebar,reverse('arbitrajes:referee_list')])
    items.setdefault("trabajos_sidebar",[trabajos_sidebar,reverse('trabajos:jobs_list')])

    # Menu de resultados

    # Menu de eventos 
    items.setdefault("eventos_sidebar_full",[eventos_sidebar_full,reverse('eventos:event_list')])
    items.setdefault("espacio_sidebar",[espacio_sidebar,reverse('sesiones:sesions_space_list')])
    

    items.setdefault("configuration",[configuration,''])
    items.setdefault("arbitration",[arbitration,''])
    items.setdefault("result",[result,''])
    items.setdefault("event",[event,''])

    return items

def get_route_configuracion(items):
    
    for item,val in items.items():
        # print item, ":", val[0]
        if ( ((item == "configuracion_general_sidebar") or (item == "usuarios_sidebar") or (item == "recursos_sidebar") or (item == "areas_subareas_sidebar") or (item == "estado_arbitrajes_sidebar") or (item == "datos_basicos_sidebar") or (item == "asignacion_coordinador_general") or (item == "asignacion_coordinador_area")) and val[0] == 1 ):
            # print item , ":" , val[1]
            return val[1]

def get_route_seguimiento(items):
    
    for item,val in items.items():
        # print item, ":", val[0]
        if ( ((item == "autores_sidebar") or (item == "arbitros_sidebar") or (item == "sesion_arbitraje_sidebar") or (item == "arbitraje_sidebar") or (item == "trabajos_sidebar") ) and val[0] == 1 ):
            # print item , ":" , val[1]
            return val[1]


# Create your views here.
def login(request):
    form = MyLoginForm()
    context = {
        'nombre_vista' : 'Login',
        'form' : form,
    }
    return render(request, 'main_app_login.html', context)

def home(request):
    # queryset
    arbitraje_data = Sistema_asovac.objects.all()
    secondary_navbar_options = ['Bienvenido']
    # print(arbitraje_data)
    context = {
        'nombre_vista' : 'Home',
        'secondary_navbar_options' : secondary_navbar_options,
        'arb_data' : arbitraje_data,
    }
    return render(request, 'main_app_home.html', context)

def create_arbitraje(request):
    form = CreateArbitrajeForm()
    context = {
                    'nombre_vista' : 'Crear Arbitraje',
                    'username' : request.user.username,
                    'form' : form,
                }
    if request.method == 'POST':
        form = CreateArbitrajeForm(request.POST or None)
        if form.is_valid():
            form.save()
            # print(form)
            arbitraje_data = Sistema_asovac.objects.all()
            context = {        
                'username' : request.user.username,
                'form' : form,
                'arb_data': arbitraje_data,
                }
            return render(request, 'main_app_home.html', context)        
        
    return render(request, 'main_app_create_arbitraje.html', context)

def email_test(request):
    context = {
        'nombre_vista' : 'Email-Test',
        'username' : 'Rabindranath Ferreira',
        'resumen_title': 'Escalamiento a escala industrial de una crema azufrada optimizada mediante un diseño experimental',
        'authors': ['Karla Calo', 'Luis Henríquez']
    }
    return render(request, 'resumen_rejected_email.html', context)

def listado_trabajos(request):
    context = {
        'nombre_vista' : 'Lista de Trabajos',
        'username' : 'Rabindranath Ferreira',
    }
    return render(request, 'main_app_resumenes_trabajos_list.html', context)

def detalles_resumen(request):
    context = {
        'nombre_vista' : 'Detalles de Resumen',
        'username' : 'Rabindranath Ferreira',
    }
    return render(request, 'main_app_detalle_resumen.html', context)


def dashboard(request):
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

    items=validate_rol_status(estado,rol_id,item_active)

    route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))
    # print items

    # for item,val in items.items():
        # print item, ":", val[0]

    context = {
        'nombre_vista' : 'Dashboard',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        'usuarios_sidebar' : items["usuarios_sidebar"][0],
        'recursos_sidebar' : items["recursos_sidebar"][0],
        'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        'autores_sidebar' : items["autores_sidebar"][0],
        'arbitros_sidebar' : items["arbitros_sidebar"][0],
        'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        'trabajos_sidebar':items["trabajos_sidebar"][0],
        'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        'espacio_sidebar':items["espacio_sidebar"][0],
        'verify_configuration':items["configuration"][0],
        'verify_arbitration':items["arbitration"][0],
        'verify_result':items["result"][0],
        'verify_event':items["event"][0],
        'route_conf':route_conf,
        'route_seg':route_seg,
    }
    return render(request, 'main_app_dashboard.html', context)

def data_basic(request):
    form= DataBasicForm()

    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=-1
        event_id= -1
    
    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()

    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    # print (rol_id)

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active)
   
    route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))
    # print items

    context = {
        'nombre_vista' : 'Configuracion general',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        'usuarios_sidebar' : items["usuarios_sidebar"][0],
        'recursos_sidebar' : items["recursos_sidebar"][0],
        'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        'autores_sidebar' : items["autores_sidebar"][0],
        'arbitros_sidebar' : items["arbitros_sidebar"][0],
        'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        'trabajos_sidebar':items["trabajos_sidebar"][0],
        'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        'espacio_sidebar':items["espacio_sidebar"][0],
        'verify_configuration':items["configuration"][0],
        'verify_arbitration':items["arbitration"][0],
        'verify_result':items["result"][0],
        'verify_event':items["event"][0],
        'route_conf':route_conf,
        'route_seg':route_seg,
    }
    return render(request, 'main_app_data_basic.html', context)

def state_arbitration(request):
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

    # print (rol_id)
    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active)

    route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))

    # print items

    

    context = {
        'nombre_vista' : 'Configuracion general',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        'usuarios_sidebar' : items["usuarios_sidebar"][0],
        'recursos_sidebar' : items["recursos_sidebar"][0],
        'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        'autores_sidebar' : items["autores_sidebar"][0],
        'arbitros_sidebar' : items["arbitros_sidebar"][0],
        'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        'trabajos_sidebar':items["trabajos_sidebar"][0],
        'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        'espacio_sidebar':items["espacio_sidebar"][0],
        'verify_configuration':items["configuration"][0],
        'verify_arbitration':items["arbitration"][0],
        'verify_result':items["result"][0],
        'verify_event':items["event"][0],
        'route_conf':route_conf,
        'route_seg':route_seg,
    }
    return render(request, 'main_app_status_arbitration.html', context)

def users_list(request):

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
        event_id= -1

    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()
    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    # print (rol_id)
    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active)

    route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))

    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        'usuarios_sidebar' : items["usuarios_sidebar"][0],
        'recursos_sidebar' : items["recursos_sidebar"][0],
        'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        'autores_sidebar' : items["autores_sidebar"][0],
        'arbitros_sidebar' : items["arbitros_sidebar"][0],
        'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        'trabajos_sidebar':items["trabajos_sidebar"][0],
        'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        'espacio_sidebar':items["espacio_sidebar"][0],
        'verify_configuration':items["configuration"][0],
        'verify_arbitration':items["arbitration"][0],
        'verify_result':items["result"][0],
        'verify_event':items["event"][0],
        'route_conf':route_conf,
        'route_seg':route_seg,
    }
    return render(request, 'main_app_users_list.html', context)
    
def register(request):
    if request.method == 'POST':
        form= RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado de manera exitosa.')
            context={"form":form,}
            return redirect('login')

        else:
            context={"form":form,}
            return render(request,'main_app_register.html',context)
            
    else:
        form = RegisterForm()
        context={"form":form,}
        return render(request,'main_app_register.html',context)

def user_edit(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=0
        event_id= -1

    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()
    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    # print (rol_id)
    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active)

    route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))
    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        'usuarios_sidebar' : items["usuarios_sidebar"][0],
        'recursos_sidebar' : items["recursos_sidebar"][0],
        'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        'autores_sidebar' : items["autores_sidebar"][0],
        'arbitros_sidebar' : items["arbitros_sidebar"][0],
        'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        'trabajos_sidebar':items["trabajos_sidebar"][0],
        'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        'espacio_sidebar':items["espacio_sidebar"][0],
        'verify_configuration':items["configuration"][0],
        'verify_arbitration':items["arbitration"][0],
        'verify_result':items["result"][0],
        'verify_event':items["event"][0],
        'route_conf':route_conf,
        'route_seg':route_seg,
    }
    return render(request, 'main_app_edit_user.html', context)

def user_roles(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['']
    if request.POST:
        estado= request.POST['estado']
        event_id= request.POST['event_id']
    else:
        estado=0
        event_id=-1

    rol = Usuario_asovac.objects.get(usuario_id=request.user.id).rol.all()

    rol_id=[]
    for item in rol:
        rol_id.append(item.id)

    # print (rol_id)
    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active)

    route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))

    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        'usuarios_sidebar' : items["usuarios_sidebar"][0],
        'recursos_sidebar' : items["recursos_sidebar"][0],
        'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        'autores_sidebar' : items["autores_sidebar"][0],
        'arbitros_sidebar' : items["arbitros_sidebar"][0],
        'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        'trabajos_sidebar':items["trabajos_sidebar"][0],
        'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        'espacio_sidebar':items["espacio_sidebar"][0],
        'verify_configuration':items["configuration"][0],
        'verify_arbitration':items["arbitration"][0],
        'verify_result':items["result"][0],
        'verify_event':items["event"][0],
        'route_conf':route_conf,
        'route_seg':route_seg,
    }
    return render(request, 'main_app_user_roles.html', context)

def coord_general(request):
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

    # print (rol_id)
    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active)

    route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))

    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        'usuarios_sidebar' : items["usuarios_sidebar"][0],
        'recursos_sidebar' : items["recursos_sidebar"][0],
        'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        'autores_sidebar' : items["autores_sidebar"][0],
        'arbitros_sidebar' : items["arbitros_sidebar"][0],
        'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        'trabajos_sidebar':items["trabajos_sidebar"][0],
        'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        'espacio_sidebar':items["espacio_sidebar"][0],
        'verify_configuration':items["configuration"][0],
        'verify_arbitration':items["arbitration"][0],
        'verify_result':items["result"][0],
        'verify_event':items["event"][0],
        'route_conf':route_conf,
        'route_seg':route_seg,
    }
    return render(request, 'main_app_coord_general.html', context)

def coord_area(request):
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

    # print (rol_id)
    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active)

    route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))
    
    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        'usuarios_sidebar' : items["usuarios_sidebar"][0],
        'recursos_sidebar' : items["recursos_sidebar"][0],
        'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        'autores_sidebar' : items["autores_sidebar"][0],
        'arbitros_sidebar' : items["arbitros_sidebar"][0],
        'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        'trabajos_sidebar':items["trabajos_sidebar"][0],
        'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        'espacio_sidebar':items["espacio_sidebar"][0],
        'verify_configuration':items["configuration"][0],
        'verify_arbitration':items["arbitration"][0],
        'verify_result':items["result"][0],
        'verify_event':items["event"][0],
        'route_conf':route_conf,
        'route_seg':route_seg,
    }
    return render(request, 'main_app_coord_area.html', context)

def total(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': True},
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

    # print (rol_id)
    item_active = 3
    items=validate_rol_status(estado,rol_id,item_active)

    route_conf= get_route_configuracion(validate_rol_status(estado,rol_id,1))
    route_seg= get_route_seguimiento(validate_rol_status(estado,rol_id,2))

    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'configuracion_general_sidebar': items["configuracion_general_sidebar"][0],
        'usuarios_sidebar' : items["usuarios_sidebar"][0],
        'recursos_sidebar' : items["recursos_sidebar"][0],
        'areas_subareas_sidebar' : items["areas_subareas_sidebar"][0],
        'autores_sidebar' : items["autores_sidebar"][0],
        'arbitros_sidebar' : items["arbitros_sidebar"][0],
        'sesion_arbitraje_sidebar' : items["sesion_arbitraje_sidebar"][0],
        'arbitraje_sidebar' : items["arbitraje_sidebar"][0],
        'eventos_sidebar_full' : items["eventos_sidebar_full"][0],
        'asignacion_coordinador_general': items["asignacion_coordinador_general"][0],
        'asignacion_coordinador_area': items["asignacion_coordinador_area"][0],
        'datos_basicos_sidebar' : items["datos_basicos_sidebar"][0],
        'trabajos_sidebar':items["trabajos_sidebar"][0],
        'estado_arbitrajes_sidebar':items["estado_arbitrajes_sidebar"][0],
        'espacio_sidebar':items["espacio_sidebar"][0],
        'verify_configuration':items["configuration"][0],
        'verify_arbitration':items["arbitration"][0],
        'verify_result':items["result"][0],
        'verify_event':items["event"][0],
        'route_conf':route_conf,
        'route_seg':route_seg,
    }
    return render(request, 'main_app_totales.html', context)