# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random, string
from decouple import config

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import ArbitrajeStateChangeForm, MyLoginForm, CreateArbitrajeForm, RegisterForm, DataBasicForm,PerfilForm,RolForm, ArbitrajeAssignCoordGenForm, AssingRolForm
from .models import Rol,Sistema_asovac,Usuario_asovac

# Lista de Estados de un arbitraje.
estados_arbitraje = [ 'Desactivado',
                      'Iniciado',
                      'En Selección y Asignación de Coordinadores de Área',
                      'En Carga de Trabajos',
                      'En Asignación de Trabajos a las Áreas',
                      'En Arbitraje',
                      'En Cierre de Arbitraje',
                      'En Asignación de Secciones',
                      'En Resumen'
                    ]

# Global functions
def validate_rol_status(estado,rol_id,item_active, arbitraje_id):
    """ Retornar un diccionario de items con 2 listas, cada una con un string por cada opción a desplegar en el frontend """
    items={}
    top_nav_options = []
    sidebar_options = []

    ### Opciones del Menu Principal ###
    # verify_configuration
    if not ( (estado == 0 and 2 in rol_id) or ((estado != 1 and estado != 8) and 3 in rol_id) or ((estado != 8) and 4 in rol_id) or 5 in rol_id):
        top_nav_options.append('configuration')
    # verify arbitration
    if not ( ((estado == 0 or estado == 8) and 2 in rol_id) or ((estado == 0 or estado == 8) and 3 in rol_id) or 4 in rol_id or 5 in rol_id):
        top_nav_options.append('arbitration')
    # verify result
    if not ( ((estado !=6 and estado != 7 and estado != 8) and 2 in rol_id) or ((estado != 6 and estado != 8) and 3 in rol_id) or ((estado != 8 and estado != 6) and 4 in rol_id) or (estado != 6 and 5 in rol_id)):
        top_nav_options.append('result')
    # verify job
    if ((estado == 3 and 5 in rol_id) or (estado == 5 and 4 in rol_id)):
        top_nav_options.append('jobs')
    # verify trabajo_options
    if(estado == 3 and 5 in rol_id):
        top_nav_options.append('job_options')

    items['top_nav_options'] = top_nav_options

    ### Opciones del Menu de la Barra Lateral o Sidebar ###
    # verify_configuracion_general_option
    if (1 in rol_id and item_active == 1) or (estado != 0 and 2 in rol_id and item_active == 1):
        sidebar_options.append("general_config")
    # verify_datos_basicos_option
    if not (estado == 2 and (1 not in rol_id and 2 not in rol_id) and item_active == 1) or (estado == 4 and (1 not in rol_id and 2 not in rol_id) and item_active ==1):
        sidebar_options.append("basic_data")
    # verify_estado_arbitrajes_option (This one is always true...)
    sidebar_options.append("arbitration_state")
    # verify_usuario_option & verify_asignacion_coordinador_general_option (same condition)
    if (1 in rol_id and item_active == 1):
        sidebar_options.append("users")
        sidebar_options.append("assing_general_coordinator")
    # verify_asignacion_coordinador_area_option
    if(estado ==2 and 2 in rol_id and item_active == 1) or (1 in rol_id and item_active == 1):
        sidebar_options.append("assing_area_coordinator")
    # verify_recursos_option
    if (1 in rol_id and item_active == 1) or (estado ==8 and (2 in rol_id or 3 in rol_id  or 4 in rol_id) and item_active==1):
        sidebar_options.append("resources")
    # verify_areas_subareas_option
    if (1 in rol_id and item_active == 1) or (estado == 1 and (2 in rol_id or 3 in rol_id) and item_active == 1) or (estado == 2 and 2 in rol_id and item_active ==1):
        sidebar_options.append("areas_subareas")
    # verify_autores_option
    if ((estado == 0 or estado ==5 or estado ==6 or estado ==7 or estado ==8) and 1 in rol_id and item_active == 2) or ((estado == 1 or estado ==2 or estado == 3 or estado == 4) and (1 in rol_id or 2 in rol_id) and item_active == 2):
        sidebar_options.append("authors")
    # verify_arbitros_option
    if (1 in rol_id and item_active == 2) or (estado == 1 and 2 in rol_id and item_active == 2) or ((estado ==2 or estado == 3 or estado == 4) and (2 in rol_id or 3 in rol_id) and item_active == 2) or (estado ==1 and 3 in rol_id and item_active==2):
        sidebar_options.append("arbiters")
    # verify_asignar_sesion
    if(1 in rol_id and item_active == 2) or (estado == 4 and (2 in rol_id or 3 in rol_id) and item_active == 2) or (estado ==7 and 2 in rol_id and item_active == 2):
        sidebar_options.append("assing_session")
    # verify_trabajo_option
    if((estado ==3 or estado ==4 or estado ==5) and (2 in rol_id or 3 in rol_id) and item_active == 2) or (1 in rol_id and item_active ==2) or(estado ==6 and 3 in rol_id and item_active ==2):
        sidebar_options.append("jobs")
    # verify_sesions_arbitraje_option
    if (1 in rol_id and item_active == 2) or ((estado == 4 or estado ==7) and (2 in rol_id or 3 in rol_id) and item_active == 2):
        sidebar_options.append("session_arbitration")
    # verify_arbitraje_option
    if (1 in rol_id and item_active == 2) or (estado ==6 and (2 in rol_id) and item_active == 2):
        sidebar_options.append("arbitrations")
    # verify_eventos_sidebar_full & verify_espacio_option (same condition)
    if (1 in rol_id and item_active == 4):
        sidebar_options.append("events")
        sidebar_options.append("event_space")

    items['sidebar_options'] = sidebar_options

    return items

def get_route_configuracion(estado,rol_id, arbitraje_id):
    if(1 in rol_id or 2 in rol_id):
        #Caso que sea admin o coordinador general
        return reverse('main_app:data_basic', kwargs={'arbitraje_id': arbitraje_id})
    elif 3 in rol_id:
        if(estado == 8):
            return reverse('recursos:resources_author')
        if(estado == 1):
            return reverse('arbitrajes:arbitrations_areas_subareas')
    elif 4 in rol_id:
        if(estado == 8):
            return reverse('recursos:resources_author')
    return None



def get_route_seguimiento(estado,rol_id):
    if 1 in rol_id:
        return reverse('autores:authors_list')
    elif 2 in rol_id:
        if(estado in [1,2,3,4]):
            return reverse('autores:authors_list')
        elif(estado == 5):
            return reverse('trabajos:jobs_list')
        elif(estado == 6):
            return reverse('arbitrajes:listado')
        elif(estado == 7):
            return reverse('arbitrajes:asignacion_de_sesion')
    elif 3 in rol_id:
        if(estado in [1,2,3,4]):
            return reverse('arbitrajes:referee_list')
        elif(estado in  [5,6]):
            return reverse('trabajos:jobs_list')
        elif(estado == 7):
            return reverse('sesiones:sesions_list')


def get_route_trabajos_sidebar(estado,rol_id,item_active):
    if (estado == 4 and 2 in rol_id and item_active == 2):
        return reverse('trabajos:trabajos_evaluados')
    else:
        return reverse('trabajos:jobs_list')


def get_route_trabajos_navbar(estado,rol_id):
    if(estado == 3 and 5 in rol_id):
        return reverse('trabajos:trabajos')
    if(estado == 5 and 4 in rol_id):
        return reverse('trabajos:trabajos_evaluados')
    return None 

def get_route_resultados(estado,rol_id, arbitraje_id):
    if(estado== 6 and 5 in rol_id):
        return reverse('trabajos:trabajos_resultados_autor')
    else:
        return reverse('main_app:total', kwargs={'arbitraje_id': arbitraje_id})

#Obtener roles del usuario
def get_roles(user_id):
    rol = Usuario_asovac.objects.get(usuario_id=user_id).rol.all()
    rol_id=[]
    for item in rol:
        rol_id.append(item.id)
    return rol_id

#Update state of arbitration
def update_state_arbitration(arbitraje_id,estado):
    new_state = Sistema_asovac.objects.get(pk=arbitraje_id)
    #update Sistema_asovac
    new_state.estado_arbitraje = estado
    # save in DB
    new_state.save()
    return estado

def compute_progress_bar(state):
    if state == 0:
        return 0
    else:
        return int(float(state) / 8.0 * 100.0)
#########################################################################################
################################## VIEWS BACKEND #######################################
########################################################################################


def login(request):
    form = MyLoginForm()
    context = {
        'nombre_vista' : 'Login',
        'form' : form,
    }
    return render(request, 'main_app_login.html', context)



def register(request):
    if request.method == 'POST':
        form= RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha registrado Exitosamente.')
            context={"form":form,}
            return redirect('login')
        else:
            context={"form":form,}
            return render(request,'main_app_register.html',context)
    else:
        form = RegisterForm()
        context={"form":form,}
        return render(request,'main_app_register.html',context)



def home(request):
    # Queryset
    arbitraje_data = Sistema_asovac.objects.all()

    rol_id=get_roles(request.user.id)

    # Lista de booleanos que indica si un arbitraje despliega o no el boton de "Entrar"
    allow_entry_list = []
    # Lista de strings de estados de los arbitrajes
    state_strings = []

    # En este ciclo for determinamos el string de estado de un arbitraje y si el usuario
    # puede o no acceder a el
    for arb in arbitraje_data:
        state_strings.append(estados_arbitraje[arb.estado_arbitraje])
        if 1 in rol_id:
            allow_entry_list.append(True)
        elif 2 in rol_id and arb.estado_arbitraje != 0:
            allow_entry_list.append(True)
        elif 3 in rol_id and arb.estado_arbitraje != 0:
            allow_entry_list.append(True)
        elif 4 in rol_id and arb.estado_arbitraje in [5,6,8]:
            allow_entry_list.append(True)
        elif 5 in rol_id and arb.estado_arbitraje in [3,6]:
            allow_entry_list.append(True)
        else:
            allow_entry_list.append(False)

    # Se le aplican zip a las 3 siguientes listas para que todas queden en una lista de tuplas
    arb_data = zip(arbitraje_data, state_strings, allow_entry_list)

    print(arbitraje_data, state_strings, allow_entry_list)
    context = {
        'nombre_vista' : 'Inicio',
        'arb_data' : arb_data,
        'rol_id' : rol_id,
    }
    return render(request, 'main_app_home.html', context)



def dashboard(request, arbitraje_id):
    ######################################################################################
    # Aquí debe ocurrir una verificacion: tiene el request.user acceso a este arbitraje?
    # Si: se procede a desplegar el contenido normalmente.
    # No: Se despliega un error 404
    ######################################################################################

    request.session['arbitraje_id'] = arbitraje_id
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    request.session['estado'] = arbitraje.estado_arbitraje

    rol_id=get_roles(request.user.id)

    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']

    item_active = 1
    #print(request.session['estado'])
    items=validate_rol_status(estado, rol_id, item_active, arbitraje_id)

    progress_pct = compute_progress_bar(arbitraje.estado_arbitraje)

    route_conf = get_route_configuracion(estado, rol_id, arbitraje_id)
    route_seg = get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
    print arbitraje.estado_arbitraje, progress_pct

    # for item,val in items.items():
        # print item, ":", val[0]

    context = {
        'nombre_vista' : 'Dashboard',
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje' : arbitraje,
        'progress_pct': progress_pct,
        'arbitraje_id' : arbitraje_id,
        'arbitraje_state': estados_arbitraje[arbitraje.estado_arbitraje],
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'main_app_dashboard.html', context)

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
            return redirect('main_app:home')        
    return render(request, 'main_app_create_arbitraje.html', context)



def email_test(request):
    context = {
        'nombre_vista' : 'Email-Test',
        'username' : 'Rabindranath Ferreira',
        'resumen_title': 'Escalamiento a escala industrial de una crema azufrada optimizada mediante un diseño erandom_passwordperimental',
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




def data_basic(request, arbitraje_id):
    form= DataBasicForm()

    ######################################################################################
    # Aquí debe ocurrir una verificacion: tiene el request.user acceso a este arbitraje?
    # Si: se procede a desplegar el contenido normalmente.
    # No: Se despliega un error 404
    ######################################################################################

    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']

    rol_id=get_roles(request.user.id)
    # print (rol_id)
    
    arbitraje = Sistema_asovac.objects.get(id = arbitraje_id)

    if request.POST:
        opcion = request.POST['generar_clave']
        random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
            
        if opcion == '1': #Caso de generar clave  para coordinador general
            random_password += 'COG'
            arbitraje.clave_maestra_coordinador_general = random_password
            arbitraje.save()
            messages.success(request, 'La contraseña de coordinador general ha sido generada.')

            usuarios = Usuario_asovac.objects.filter(Sistema_asovac_id = arbitraje.id, rol = 2) | Usuario_asovac.objects.filter(Sistema_asovac_id = arbitraje.id, rol = 1) 
            nombre_sistema = Sistema_asovac.objects.get(id=request.session['arbitraje_id']).nombre
            nombre_rol = Rol.objects.get(id=2).nombre
            context = {
            'rol': nombre_rol,
            'sistema': nombre_sistema,
            'password': random_password,
            }
            msg_plain = render_to_string('../templates/email_templates/password_generator.txt', context)
            msg_html = render_to_string('../templates/email_templates/password_generator.html', context)
            
            for item in usuarios:
                
                send_mail(
                        'Asignación de contraseña',         #titulo
                        msg_plain,                          #mensaje txt
                        config('EMAIL_HOST_USER'),          #email de envio
                        [item.usuario.email],               #destinatario
                        html_message=msg_html,              #mensaje en html
                        )

        
        elif opcion == '2':#Caso de generar clave para coordinador de area
            random_password += 'COA'
            arbitraje.clave_maestra_coordinador_area = random_password
            arbitraje.save()
            messages.success(request, 'La contraseña de coordinador de area ha sido generada.')

            usuarios = Usuario_asovac.objects.filter(Sistema_asovac_id = arbitraje.id, rol = 3) | Usuario_asovac.objects.filter(Sistema_asovac_id = arbitraje.id, rol = 1) 
            nombre_sistema = Sistema_asovac.objects.get(id=request.session['arbitraje_id']).nombre
            nombre_rol = Rol.objects.get(id=3).nombre
            context = {
            'rol': nombre_rol,
            'sistema': nombre_sistema,
            'password': random_password,
            }
            msg_plain = render_to_string('../templates/email_templates/password_generator.txt', context)
            msg_html = render_to_string('../templates/email_templates/password_generator.html', context)
            
            for item in usuarios:
                
                send_mail(
                        'Asignación de contraseña',         #titulo
                        msg_plain,                          #mensaje txt
                        config('EMAIL_HOST_USER'),          #email de envio
                        [item.usuario.email],               #destinatario
                        html_message=msg_html,              #mensaje en html
                        )
        

        elif opcion == '3':#Caso de generar clave para arbitro de subarea
            random_password += 'ARS'
            arbitraje.clave_maestra_arbitro_subarea = random_password
            arbitraje.save()
            messages.success(request, 'La contraseña de arbitro de subarea ha sido generada.')

            usuarios = Usuario_asovac.objects.filter(Sistema_asovac_id = arbitraje.id, rol = 4) | Usuario_asovac.objects.filter(Sistema_asovac_id = arbitraje.id, rol = 1) 
            nombre_sistema = Sistema_asovac.objects.get(id=request.session['arbitraje_id']).nombre
            nombre_rol = Rol.objects.get(id=4).nombre
            context = {
            'rol': nombre_rol,
            'sistema': nombre_sistema,
            'password': random_password,
            }
            msg_plain = render_to_string('../templates/email_templates/password_generator.txt', context)
            msg_html = render_to_string('../templates/email_templates/password_generator.html', context)
            
            for item in usuarios:
                
                send_mail(
                        'Asignación de contraseña',         #titulo
                        msg_plain,                          #mensaje txt
                        config('EMAIL_HOST_USER'),          #email de envio
                        [item.usuario.email],               #destinatario
                        html_message=msg_html,              #mensaje en html
                        )
        

        print("The password is:"+random_password)



    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active,arbitraje_id)

    route_conf = get_route_configuracion(estado,rol_id,arbitraje_id)
    route_seg = get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items

    context = {
        'nombre_vista' : 'Configuracion general',
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'arbitraje':arbitraje,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'main_app_data_basic.html', context)

def state_arbitration(request, arbitraje_id):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol_id=get_roles(request.user.id)

    # print (rol_id)
    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']
    user_id = request.user.id

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf = get_route_configuracion(estado,rol_id)
    route_seg = get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # si se envia el cambio de estado via post se actualiza en bd
    # if request.method == 'POST':
    #     estado = request.POST['estado']
    #     #print(estado)
    #     request.session['estado'] = update_state_arbitration(arbitraje_id,estado)

    # Preparamos el formulario y el proceso de este para asignar coordinador general.
    arbitraje = get_object_or_404(Sistema_asovac,id=arbitraje_id)
    form = ArbitrajeStateChangeForm(request.POST or None, instance = arbitraje)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        else:
            print (form.errors)
        #estado = request.POST['estadoArbitraje']
        #print(estado)
        #request.session['estado'] = update_state_arbitration(arbitraje_id,estado)


    # si entro en el post se actualiza el estado de lo contrario no cambia y se lo paso a la vista igualmente        
    estado = request.session['estado']
    context = {
        'nombre_vista' : 'Configuracion general',
        'main_navbar_options' : main_navbar_options,
        'estado' : estado,
        'form':form,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'main_app_status_arbitration.html', context)

def users_list(request, arbitraje_id):

    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


    rol_id = get_roles(request.user.id)
    users = User.objects.all()
    
    # rol = Usuario_asovac.objects.get(usuario_id=user.id).rol.all()
    user_asovac = Usuario_asovac.objects.all()
    users = Usuario_asovac.objects.all()

    for user in user_asovac:
        query = user.usuario.username
        user.rol.all()
        # for rol in user.rol.all():
        #user.area_id.all()
        #print (query)

    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']

    item_active = 1
    items = validate_rol_status(estado,rol_id,item_active)

    route_conf = get_route_configuracion(estado,rol_id)
    route_seg = get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'users' : users,
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'main_app_users_list.html', context)



def user_edit(request, arbitraje_id):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol_id=get_roles(request.user.id)

    # print (rol_id)
    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'main_app_edit_user.html', context)



def user_roles(request, arbitraje_id):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol_id=get_roles(request.user.id)

    # print (rol_id)
    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'main_app_user_roles.html', context)



def coord_general(request, arbitraje_id):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol_id=get_roles(request.user.id)

    # print (rol_id)
    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items

    # Preparamos el formulario y el proceso de este para asignar coordinador general.
    arbitraje = get_object_or_404(Sistema_asovac,id=arbitraje_id)
    form = ArbitrajeAssignCoordGenForm(request.POST or None, instance = arbitraje)
    if request.method == 'POST':
        if form.is_valid():
            form.save()

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'estado' : estado,
        'rol_id' : rol_id,
        'form': form,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'main_app_coord_general.html', context)




def coord_area(request, arbitraje_id):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol_id=get_roles(request.user.id)

    # print (rol_id)
    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
    
    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'main_app_coord_area.html', context)

def total(request, arbitraje_id):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': True},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    rol_id=get_roles(request.user.id)

    # print (rol_id)
    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']
    
    item_active = 3
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items

    context = {
        'nombre_vista' : 'Usuarios',
        'main_navbar_options' : main_navbar_options,
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'main_app_totales.html', context)

def apps_selection(request):
    # queryset
    # arbitraje_data = Sistema_asovac.objects.all()

    # if request.method == 'POST':
    #     context = {
    #         'nombre_vista' : 'Home',
    #         'arb_data' : arbitraje_data,
    #     }
    #     return render(request, 'main_app_home.html',context)
    context = {
    
    }

    return render(request, 'main_app_aplicaciones_opc.html',context)

# Ajax/para el uso de ventanas modales
def process_modal(request,form,template_name):
    data= dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid']= True
            # users= User.objects.all()
            users= Usuario_asovac.objects.all()
            data['user_list']= render_to_string('ajax/dinamic_list.html',{'users':users})
        else:
            data['form_is_valid']= False
  
    context={
        'form': form
    }
    data['html_form']= render_to_string(template_name,context, request=request)
    return JsonResponse(data)

def create_user_modal(request):
    if request.method == 'POST':
        form= RegisterForm(request.POST)
    else:
        form= RegisterForm()

    return process_modal(request,form,'ajax/users-create.html')

def update_user_modal(request,id):
    print "update_user_modal"
    user=  get_object_or_404(User,id=id)
    if request.method == 'POST':
        # form= RegisterForm(request.POST,instance=user)
        form= PerfilForm(request.POST,instance=user)
    else:
        # form= RegisterForm(instance=user)
        form= PerfilForm(instance=user)
    return process_modal(request,form,'ajax/user_update.html')
    
def delete_user_modal(request,id):
    data= dict()
    user= get_object_or_404(User,id=id)
    # print user
    if request.method == 'POST':
        user.delete()
        data['form_is_valid']= True
        # users= User.objects.all()
        users= Usuario_asovac.objects.all()
        data['user_list']= render_to_string('ajax/dinamic_list.html',{'users':users})
    else:
        context= {'user':user}
        data['html_form']=render_to_string('ajax/user_delete.html',context,request=request)

    return JsonResponse(data)

def update_rol_modal(request,id):
    #print "update_rol_modal"
    data= dict()
    # Obtenemos el mayor rol del usuario que hizo la petición
    request_user = request.user
    request_user_role = request_user.usuario_asovac.biggest_role()
    # Obtenemos la instancia del usuario asovac a modificar y su mayor rol
    user= get_object_or_404(Usuario_asovac,id=id)
    user_role = user.biggest_role()

    form = None
    if request.method == 'POST':
        # Este formulario tiene todas las opciones populadas de acuerdo al formulario enviado por POST.
        form = form = AssingRolForm(request.POST, instance = user, max_role = 0)
        if form.is_valid():
            form.save()
            data['form_is_valid']= True

        users= Usuario_asovac.objects.all()
        data['user_list']= render_to_string('ajax/dinamic_list.html',{'users':users})

    else:
        if request_user.id is user.id and request_user_role.id < 4:
            # Si el usuario haciendo la petición coincide con el usuario a ser editado:
            # Se despliegan opciones de rol hasta su propio máximo rol.
            form = AssingRolForm(instance = user, max_role = request_user_role.id - 1)
            context={'form': form, 'user':user}
            data['html_form']= render_to_string('ajax/rol_update.html',context, request=request)
        elif (request_user_role.id < user_role.id and request_user_role.id < 4):
            # Si el rol del usuario haciendo la petición es mayor en rango al del usuario ser editado y este tiene un rol con permiso
            # para modificar: Se despliegan opciones hasta el rol por debajo del mayor rol del usuario haciendo la peticion.
            form = AssingRolForm(instance = user, max_role = request_user_role.id )
            context={'form': form, 'user':user}
            data['html_form']= render_to_string('ajax/rol_update.html',context, request=request)
        else:
            # Sino solo se despliega la informacion de los roles del usuario a modificar.
            context={'user': user}
            data['html_form']= render_to_string('ajax/rol_read.html',context, request=request)

    return JsonResponse(data)
