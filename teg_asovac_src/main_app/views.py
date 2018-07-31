# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .forms import MyLoginForm, CreateArbitrajeForm, RegisterForm, DataBasicForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from .models import Rol,Sistema_asovac,Usuario_asovac

# Global functions
# Esta función verifica que se va a desplegar la opción de configuracion general en el sidebar, retorna 1 si se usará y 0 sino.
def verify_configuracion_general_option(estado, rol_id, item_active): 
    if ((estado == '0' or estado =='1' or estado =='3') and 1 in rol_id and item_active == 1) or (estado =='2' and (1 in rol_id or 2 in rol_id) and item_active == 1):
        return 1
    return 0

def verify_datos_basicos_option(estado,rol_id,item_active):
    if(estado == '2' and (1 not in rol_id and 2 not in rol_id) and item_active == 1):
        return 0
    return 1


def verify_usuario_option(estado,rol_id, item_active):
    if ((estado == '0' or estado =='1' or estado =='2' or estado == '3') and 1 in rol_id and item_active == 1):
        return 1
    return 0


def verify_asignacion_coordinador_general_option(estado,rol_id,item_active):
    if((estado == '1' or estado =='2' or estado == '3') and  1 in rol_id and item_active == 1):
        return 1
    return 0


def verify_asignacion_coordinador_area_option(estado,rol_id,item_active):
    if(estado =='2' and  (1 in rol_id or 2 in rol_id) and item_active ==1) or(estado == '3' and 1 in rol_id and item_active == 1):
        return 1
    return 0




def verify_recursos_option(estado,rol_id,item_active):
    if ((estado == '0' or estado == '1' or estado == '2' or estado == '3') and 1 in rol_id and item_active == 1):
        return 1
    return 0

def verify_areas_subareas_option(estado,rol_id,item_active):
    if ((estado == '0' or estado =='3') and 1 in rol_id and item_active == 1) or (estado == '1' and (1 in rol_id or 2 in rol_id or 3 in rol_id) and item_active == 1) or (estado == '2' and (1 in rol_id or 2 in rol_id) and item_active ==1):
        return 1
    return 0


def verify_autores_option(estado,rol_id,item_active):
    if (estado == '0' and 1 in rol_id and item_active == 2) or ((estado == '1' or estado =='2' or estado == '3') and (1 in rol_id or 2 in rol_id) and item_active == 2):
        return 1
    return 0

def verify_arbitros_option(estado,rol_id, item_active):
    if (estado == '0' and 1 in rol_id and item_active == 2) or ((estado == '1' or estado =='2' or estado == '3') and (1 in rol_id or 2 in rol_id or 3 in rol_id) and item_active ==2):
        return 1
    return 0

def verify_sesions_arbitraje_option(estado,rol_id, item_active):
    if ((estado == '0' or estado =='1' or estado == '2' or estado == '3') and 1 in rol_id and item_active == 2):
        return 1
    return 0

def verify_arbitraje_option(estado,rol_id, item_active):
    if ((estado == '0' or estado =='1' or estado == '2' or estado == '3') and 1 in rol_id and item_active == 2):
        return 1
    return 0

def verify_trabajo_option(estado, rol_id,item_active):
    if(estado =='3' and (1 in rol_id or 2 in rol_id or 3 in rol_id) and item_active == 2):
        return 1
    return 0

def verify_eventos_sidebar_full(estado,rol_id,item_active):
    if ((estado == '0' or estado =='1' or estado == '2' or estado == '3') and 1 in rol_id and item_active == 4):
        return 1
    return 0

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
    print(arbitraje_data)
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
            #print(form)
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
   
    # print "Rol:"
    # print (rol)
    # print "User ID:"
    # print (request.user.id)
    # print "Estado:"
    # print (estado)
    # print "Evento id:"
    # print (event_id)
    
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
    # queryset del estado del proceso
    #data = Sistema_asovac.objects.get(pk=arb_id)
    print(configuracion_general_sidebar)
    context = {
        'nombre_vista' : 'Dashboard',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : '1',
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
    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'username' : 'Username',
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : '1',
        'form' : form,
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
    context = {
        'nombre_vista' : 'Administración',
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
    context = {
        'nombre_vista' : 'Administración',
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
    context = {
        'nombre_vista' : 'Administración',
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
    context = {
        'nombre_vista' : 'Administración',
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
    context = {
        'nombre_vista' : 'Administración',
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

    print (rol_id)
    item_active = 1
    configuracion_general_sidebar = verify_configuracion_general_option(estado, rol_id, item_active)
    usuarios_sidebar = verify_usuario_option(estado,rol_id,item_active)
    recursos_sidebar = verify_recursos_option(estado,rol_id,item_active)
    areas_subareas_sidebar = verify_areas_subareas_option(estado,rol_id,item_active)
    context = {
        'nombre_vista' : 'Administración',
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

    print (rol_id)
    item_active = 3
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
    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : estado,
        'rol' : rol,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : '3',
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
    }
    return render(request, 'main_app_totales.html', context)