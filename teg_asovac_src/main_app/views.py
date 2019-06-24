# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
import random, string,xlrd,os,sys,xlwt
from openpyxl import Workbook
from django.contrib.auth.hashers import make_password
from decouple import config
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template.loader import render_to_string
from django.urls import reverse
import json
from django.db.models import Q
from django.db.models import Count
from django.utils.crypto import get_random_string

from .forms import ChangePassForm, ArbitrajeStateChangeForm, MyLoginForm, CreateArbitrajeForm, RegisterForm, DataBasicForm,PerfilForm,ArbitrajeAssignCoordGenForm,SubAreaRegistForm,UploadFileForm,AreaCreateForm, AssingRolForm

from .models import Rol,Sistema_asovac,Usuario_asovac, Area, Sub_area, Usuario_rol_in_sistema
from autores.models import Autores_trabajos
from sesiones.models import Sesion
from trabajos.models import Trabajo

from arbitrajes.models import Arbitro #,Arbitros_Sistema_asovac

from autores.models import Autor, Universidad
from autores.forms import AuthorCreateAutorForm
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
    if not ( (estado == 0 and 2 == rol_id) or ((estado != 1 and estado != 8) and 3 == rol_id) or ((estado != 8) and 4 == rol_id) or 5 == rol_id):
        top_nav_options.append('configuration')

    # verify arbitration
    if not ( ((estado == 0 or estado == 8) and 2 == rol_id) or ((estado == 0 or estado == 8) and 3 == rol_id) or 4 == rol_id or 5 == rol_id):
        top_nav_options.append('arbitration')
        top_nav_options.append('area/subarea')
    # verify result
    if not ( ((estado !=6 and estado != 7 and estado != 8) and 2 == rol_id) or ((estado != 6 and estado != 8) and 3 == rol_id) or ((estado != 8 and estado != 6) and 4 == rol_id) or (estado != 6 and 5 == rol_id)):
        top_nav_options.append('result')
    # verify job
    if ((estado in [3,5] and 5 >= rol_id) or (estado == 5 and 4 >= rol_id)):
        top_nav_options.append('jobs')
    # verify trabajo_options
    if((estado == 3 or estado == 5 )and 5 >= rol_id):
        top_nav_options.append('job_options')

    items['top_nav_options'] = top_nav_options

    ### Opciones del Menu de la Barra Lateral o Sidebar ###
    # verify_configuracion_general_option
    if (1 >= rol_id and item_active == 1) or (estado != 0 and 2 >= rol_id and item_active == 1):
        sidebar_options.append("general_config")
    # verify_datos_basicos_option
    if not (estado == 2 and (1 != rol_id and 2 != rol_id) and item_active == 1) or (estado == 4 and (1 != rol_id and 2 != rol_id) and item_active ==1):
        sidebar_options.append("basic_data")
    # verify_estado_arbitrajes_option (This one is always true...)
    sidebar_options.append("arbitration_state")
    # verify_usuario_option & verify_asignacion_coordinador_general_option (same condition)
    if (1 >= rol_id and item_active == 1):
        sidebar_options.append("users")
        sidebar_options.append("assing_general_coordinator")
    # verify_asignacion_coordinador_area_option
    if(estado ==2 and 2 >= rol_id and item_active == 1) or (1 >= rol_id and item_active == 1):
        sidebar_options.append("assing_area_coordinator")
    # verify_recursos_option
    if (1 >= rol_id and item_active == 1) or (estado ==8 and (2 >= rol_id or 3 >= rol_id  or 4 >= rol_id) and item_active==1):
        sidebar_options.append("resources")
    # verify_areas_subareas_option
    if (1 >= rol_id and item_active == 1) or (estado == 1 and (2 >= rol_id or 3 >= rol_id) and item_active == 1) or (estado == 2 and 2 >= rol_id and item_active ==1):
        sidebar_options.append("areas_subareas")
    # verify_autores_option
    if ((estado == 0 or estado ==5 or estado ==6 or estado ==7 or estado ==8) and 1 >= rol_id and item_active == 2) or ((estado == 1 or estado ==2 or estado == 3 or estado == 4) and (1 >= rol_id or 2 >= rol_id) and item_active == 2):
        sidebar_options.append("authors")
    # verify_arbitros_option
    if (1 >= rol_id and item_active == 2) or (estado == 1 and 2 >= rol_id and item_active == 2) or ((estado ==2 or estado == 3 or estado == 4) and (2 >= rol_id or 3 >= rol_id) and item_active == 2) or (estado ==1 and 3 >= rol_id and item_active==2):
        sidebar_options.append("arbiters")
    # verify_asignar_sesion
    if(1 >= rol_id and item_active == 2) or (estado == 4 and (2 >= rol_id or 3 >= rol_id) and item_active == 2) or (estado ==7 and 2 >= rol_id and item_active == 2):
        sidebar_options.append("assing_session")
    # verify_trabajo_option
    if((estado ==3 or estado ==4 or estado ==5) and (2 >= rol_id or 3 >= rol_id) and item_active == 2) or (1 >= rol_id and item_active ==2) or(estado ==6 and 3 >= rol_id and item_active ==2):
        sidebar_options.append("jobs")
    # verify_sesions_arbitraje_option
    if (1 >= rol_id and item_active == 2) or ((estado == 4 or estado ==7) and (2 >= rol_id or 3 >= rol_id) and item_active == 2):
        sidebar_options.append("session_arbitration")
    # verify_arbitraje_option
    if (1 >= rol_id and item_active == 2) or (estado ==6 and (2 >= rol_id) and item_active == 2):
        sidebar_options.append("arbitrations")
    # verify_eventos_sidebar_full & verify_espacio_option (same condition)
    if (1 >= rol_id and item_active == 4):
        sidebar_options.append("events")
        sidebar_options.append("event_space")

    items['sidebar_options'] = sidebar_options

    return items

def get_route_configuracion(estado,rol_id, arbitraje_id):
    if(1 == rol_id or 2 == rol_id):
        #Caso que sea admin o coordinador general
        return reverse('main_app:data_basic', kwargs={'arbitraje_id': arbitraje_id})
    elif 3 == rol_id:
        if(estado == 8):
            return reverse('recursos:resources_author')
        if(estado == 1):
            return reverse('main_app:arbitrations_areas_subareas')
    elif 4 == rol_id:
        if(estado == 8):
            return reverse('recursos:resources_author')
    return None



def get_route_seguimiento(estado,rol_id):
    if 1 == rol_id:
        return reverse('autores:authors_list')
    elif 2 == rol_id:
        if(estado in [1,2,3,4]):
            return reverse('autores:authors_list')
        elif(estado == 5):
            return reverse('trabajos:jobs_list')
        elif(estado == 6):
            return reverse('arbitrajes:listado')
        elif(estado == 7):
            return reverse('arbitrajes:asignacion_de_sesion')
    elif 3 == rol_id:
        if(estado in [1,2,3,4]):
            return reverse('arbitrajes:referee_list')
        elif(estado in  [5,6]):
            return reverse('trabajos:jobs_list')
        elif(estado == 7):
            return reverse('sesiones:sesions_list')


def get_route_trabajos_sidebar(estado,rol_id,item_active):
    if (estado == 4 and 2 == rol_id and item_active == 2):
        return reverse('trabajos:trabajos_evaluados')
    else:
        return reverse('trabajos:jobs_list')


def get_route_trabajos_navbar(estado,rol_id):
    if((estado == 3 or estado == 5)and 5 == rol_id):
        return reverse('trabajos:trabajos')
    else:
        return None 

def get_route_resultados(estado,rol_id, arbitraje_id):
    if(estado== 6 and 5 == rol_id):
        return reverse('trabajos:trabajos_resultados_autor')
    else:
        return reverse('main_app:total', kwargs={'arbitraje_id': arbitraje_id})

# Para obtener el rol de mayor permisos asociado a un arbitraje
def get_roles(user_id, arbitraje_id):
    # Variables para validaciones
    user = get_object_or_404(User, id = user_id)
    usuario_asovac = get_object_or_404(Usuario_asovac, usuario = user)
    # is_admin se envia para saber si el usuario es administrador
    if arbitraje_id != "is_admin":
        arbitraje = get_object_or_404(Sistema_asovac, id = arbitraje_id)

    # Se verifica que tenga un rol y pertenezca a un arbitraje
    has_rol= Usuario_rol_in_sistema.objects.filter(usuario_asovac = usuario_asovac).exists()
    # is_admin se envia para saber si el usuario es administrador
    if arbitraje_id != "is_admin":
        has_arbitraje = Usuario_rol_in_sistema.objects.filter(sistema_asovac = arbitraje, usuario_asovac = usuario_asovac).exists()
    else:
        has_arbitraje = False
        
    rol_id= 6

    # Se verifica que exista el rol y un arbitraje asociado
    if has_rol == True and has_arbitraje:
        rols=Usuario_rol_in_sistema.objects.filter(sistema_asovac = arbitraje, usuario_asovac = usuario_asovac)
        rol= getMaxRol(rol_id, rols)
        if rol.status == True:
            rol_id=rol.rol_id
            # print "Tiene rol y arbitraje. El mayor rol es: ",rol.rol_id, " y el estatus es: ", rol.status
    else:
        if has_rol:
            # Para verificar que el rol del usuario es de administrador o coordinador general y este activo
            rols=Usuario_rol_in_sistema.objects.filter(usuario_asovac = usuario_asovac)
            rol= getMaxRol(rol_id, rols)
            if (rol.rol_id == 1 or rol.rol_id == 2 ) and rol.status == True:
                rol_id=rol.rol_id
                # print "Tiene rol y arbitraje. El mayor rol es: ",rol.rol_id, " y el estatus es: ", rol.status

    return rol_id

# Para obtener la lista de roles 
def get_role_list(user,arbitraje):
    admin= get_roles(user,"is_admin")
    user_asovac= get_object_or_404(Usuario_asovac, usuario = user)
    # print "usuario asovac: ",user_asovac.id
    if(admin == 1):
        # Lista de roles
        rol_active= Usuario_rol_in_sistema.objects.filter(usuario_asovac = user_asovac,status=True)
    else:
        # Lista de roles
        rol_active= Usuario_rol_in_sistema.objects.filter(usuario_asovac = user_asovac, sistema_asovac=arbitraje,status=True)
    
    rols=[]
    for item in rol_active:
        rols.append(item.rol_id)
    # print "Los roles activos son: ",rols
    return rols

# Obtener el rol de mayor privilegio
def getMaxRol(rol, roles):
    Rol= roles[0]
    for item in roles:
        if Rol.rol_id > item.rol_id:
            rol=item
    return Rol 

# Obtener nombre de los roles del usuario
def get_names_roles(user_id,name=True):
    usuario_asovac = Usuario_asovac.objects.get(usuario_id=user_id)
    big_rol=None

    # Manejo de roles
    rol_id=6
    rols=Usuario_rol_in_sistema.objects.filter(usuario_asovac_id = usuario_asovac.id)
    big_rol= getMaxRol(rol_id, rols)
    # big_rol.rol.nombre
    # print "El mayor rol es: ",big_rol.rol_id, " y el estatus es: ", big_rol.status, " y el nombre del rol es ",big_rol.rol.nombre
    if name == True:
        # Para retornar el nombre del rol
        rol_name=big_rol.rol.nombre
        big_rol=rol_name
    else:
        # para retornar el id del rol
        rol_id=big_rol.rol.id
        big_rol=rol_id

    return big_rol

#Update state of arbitration
def update_state_arbitration(arbitraje_id,estado):
    new_state = Sistema_asovac.objects.get(pk=arbitraje_id)
    #update Sistema_asovac
    new_state.estado_arbitraje = estado
    # save in DB
    new_state.save()
    return estado

#Verifica si el usuario tiene rol de admin
def is_admin(rol):
    if rol == 1:
        return 1
    else:
        return 0

#Validar accesos segun rol clave y arbitraje seleccionado
def validate_access(rol,data_arbitraje,clave):
    
    if rol == '2':
        if clave == data_arbitraje.clave_maestra_coordinador_general:
            return 1
    else:
        if rol == '3':
            if clave == data_arbitraje.clave_maestra_coordinador_area:
                return 1
        else:
            if rol == '4':
                if clave == data_arbitraje.clave_maestra_arbitro_subarea:
                    return 1
            else:
                if rol == '5':
                    return 1
    
    return 0

# Parametros para validacion de arbitraje
def create_params_validations(request,status):
    params_validations = dict()
    params_validations['rol_name']=get_names_roles(request.user.id)
    # params_validations['cant']=len(params_validations['rol_name'])
    params_validations['rol_id']=get_names_roles(request.user.id,False)
    params_validations['is_admin']=is_admin( params_validations['rol_name'])
    params_validations['status']=status
    # print params_validations
    return params_validations

# Para guardar el archivo recibido del formulario  
def save_file(request,type_load):

    name= str(request.FILES.get('file')).decode('UTF-8')
    file_name=''

    if type_load == "usuarios":   
        extension = name.split('.')        	
        file_name= "cargaUsuarios."+extension[1]
        # Permite guardar el archivo y asignarle un nombre
        handle_uploaded_file(request.FILES['file'], file_name)
        route= "upload/"+file_name
    # print "Ruta del archivo: ",route
    return route

# Para obtener la extension del archivo
def get_extension_file(filename):

    extension = filename.split('.')
    return extension[1] 

def compute_progress_bar(state):
    if state == 0:
        return 0
    else:
        return int(float(state) / 8.0 * 100.0)

#---------------------------------------------------------------------------------#
#                            VIEWS BACKEND                                        #
#---------------------------------------------------------------------------------#
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
        form2=SubAreaRegistForm(request.POST)
        if form.is_valid():
            user= form.save()
            usuario_asovac= Usuario_asovac.objects.get(usuario_id=user.id)
            # Para crear instancia de arbitro
            arbitro =Arbitro()
            arbitro.nombres=user.first_name
            arbitro.apellidos=user.last_name
            arbitro.correo_electronico=user.email
            arbitro.usuario=usuario_asovac
            arbitro.save()

            subarea= request.POST.getlist("subarea_select")
            for item in subarea:
                usuario_asovac.sub_area.add(Sub_area.objects.get(id=item))
            usuario_asovac.save()
            messages.success(request, 'Se ha registrado Exitosamente.')
            context={"form":form,}
            return redirect('login')
            
        else:
            areas= Area.objects.all()
            subareas= Sub_area.objects.all()
            # form = RegisterForm()
            subareaform=SubAreaRegistForm()
            context={
                    "form":form,
                    "subareaform":form2,
                    "areas":areas,
                    "subareas":subareas,
                }
            return render(request,'main_app_register.html',context)
    else:
        areas= Area.objects.all()
        subareas= Sub_area.objects.all()
        form = RegisterForm()
        subareaform=SubAreaRegistForm()
        context={
                "form":form,
                "subareaform":subareaform,
                "areas":areas,
                "subareas":subareas,
            }
        
        return render(request,'main_app_register.html',context)



@login_required
def home(request):
    # Queryset
    arbitraje_data = Sistema_asovac.objects.all()

    params_validations = dict()
    #rol_id=get_roles(request.user.id)
    #rol_name=get_names_roles(request.user.id)

    #params_validations['rol_name']=get_names_roles(request.user.id)
    #params_validations['cant']=params_validations['rol_name']
    #params_validations['is_admin']=is_admin( params_validations['rol_name'])
    admin=rol_id = get_roles(request.user.id ,"is_admin")
    
    params_validations['is_admin']= is_admin(admin)

    # Lista de booleanos que indica si un arbitraje despliega o no el boton de "Entrar"
    allow_entry_list = []
    # Lista de strings de estados de los arbitrajes
    state_strings = []

    #Lista de roles que tiene el usuario en el sistema, si no tiene un rol asignado en el sistema se retorna 6 para que no entre en ningún estado
    rol_list = []

    # En este ciclo for determinamos el string de estado de un arbitraje y si el usuario
    # puede o no acceder a el
    for arb in arbitraje_data:
        rol_id = get_roles(request.user.id , arb.id)
        rol_list.append(rol_id)
        state_strings.append(estados_arbitraje[arb.estado_arbitraje])
        if 1 == rol_id:
            allow_entry_list.append(True)
        elif 2 >= rol_id and arb.estado_arbitraje != 0:
            allow_entry_list.append(True)
        elif 3 >= rol_id and arb.estado_arbitraje != 0:
            allow_entry_list.append(True)
        elif 4 >= rol_id and arb.estado_arbitraje in [5,6,8]:
            allow_entry_list.append(True)
        elif 5 >= rol_id and arb.estado_arbitraje in [3,5,6]:
            allow_entry_list.append(True)
        else:
            allow_entry_list.append(False)

    # Se le aplican zip a las 3 siguientes listas para que todas queden en una lista de tuplas
    arb_data = zip(arbitraje_data, state_strings, allow_entry_list,rol_list)

    print(arbitraje_data, state_strings, allow_entry_list,rol_list)
    context = {
        'nombre_vista' : 'Inicio',
        'arb_data' : arb_data,
        'params_validations' : params_validations,
    }
    
    return render(request, 'main_app_home.html', context)



@login_required
def dashboard(request, arbitraje_id):
    #-----------------------------------------------------------------------------------#
    # Aquí debe ocurrir una verificacion: tiene el request.user acceso a este arbitraje?
    # Si: se procede a desplegar el contenido normalmente.
    # No: Se despliega un error 404
    #-----------------------------------------------------------------------------------#

    user_id= request.user.id
    user= get_object_or_404(Usuario_asovac,usuario_id=user_id)
    # para enviar area a la cual pertenece el usuari por sesion 
    subareas= user.sub_area.all()
    # area y subarea a enviar por sesion 
    area_session=subareas.first().area.nombre
    subarea_session=subareas.first().nombre
    request.session['area']= area_session
    request.session['subarea']=subarea_session

    request.session['arbitraje_id'] = arbitraje_id
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    request.session['estado']=estado

    rol_id=get_roles(request.user.id, arbitraje.id)
    arbitraje_id = request.session['arbitraje_id']

    try:
        autor = Autor.objects.get( usuario = user )
        request.session['is_author_created'] = True
    except:
        request.session['is_author_created'] = False

    item_active = 1
    #print(request.session['estado'])
    items=validate_rol_status(estado, rol_id, item_active, arbitraje_id)

    progress_pct = compute_progress_bar(arbitraje.estado_arbitraje)

    route_conf = get_route_configuracion(estado, rol_id, arbitraje_id)
    route_seg = get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # for item,val in items.items():
        # print item, ":", val[0]

    context = {
        'nombre_vista' : 'Panel Principal del Arbitraje',
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



@login_required
def create_arbitraje(request):
    form = CreateArbitrajeForm(request.POST or None)
    context = {
        'nombre_vista' : 'Crear un Arbitraje',
        'username' : request.user.username,
        'form' : form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # print(form)
            arbitraje_data = Sistema_asovac.objects.all()
            context['arb_data'] = arbitraje_data
            return redirect('main_app:home')
    return render(request, 'main_app_create_arbitraje.html', context)



def email_test(request):
    context = {
        'nombre_vista' : 'Email-Test',
        'username' : 'Rabindranath Ferreira',
        'resumen_title': 'Escalamiento a escala industrial de una crema azufrada optimizada mediante un diseño experimental',
        'authors': ['Karla Calo', 'Luis Henríquez']
    }
    return render(request, 'resumen_rejected_email.html', context)


@login_required
def listado_trabajos(request):
    context = {
        'nombre_vista' : 'Listado de Trabajos',
        'username' : 'Rabindranath Ferreira',
    }
    return render(request, 'main_app_resumenes_trabajos_list.html', context)



@login_required
def detalles_resumen(request):
    context = {
        'nombre_vista' : 'Detalles de Trabajo',
        'username' : 'Rabindranath Ferreira',
    }
    return render(request, 'main_app_detalle_resumen.html', context)



@login_required
def data_basic(request, arbitraje_id):
    #------------------------------------------------------------------------------------#
    # Aquí debe ocurrir una verificacion: tiene el request.user acceso a este arbitraje?
    # Si: se procede a desplegar el contenido normalmente.
    # No: Se despliega un error 404
    #------------------------------------------------------------------------------------#

    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id =get_roles(request.user.id,arbitraje_id)
    arbitraje = Sistema_asovac.objects.get(id = arbitraje_id)

    form = DataBasicForm(request.POST or None, instance=arbitraje)
    if request.method == 'POST':
        print('Request es POST')
        if form.is_valid():
            print('formulario es valido')
            form.save()
            messages.success(request, 'Los datos del arbitraje han sido guardados con éxito.')
            return redirect('main_app:data_basic', arbitraje_id=arbitraje_id)
        print(form.errors)

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active,arbitraje_id)
    route_conf = get_route_configuracion(estado,rol_id,arbitraje_id)
    route_seg = get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
    permiso_clave_AS = Usuario_rol_in_sistema.objects.filter(sistema_asovac = arbitraje, rol = 4).exists()
    permiso_clave_COA = Usuario_rol_in_sistema.objects.filter(sistema_asovac = arbitraje, rol = 3).exists()
    permiso_clave_COG = Usuario_rol_in_sistema.objects.filter(sistema_asovac = arbitraje, rol = 2).exists()
    context = {
        'nombre_vista' : 'Editar Configuración General',
        'form': form,
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
        'permiso_clave_AS': permiso_clave_AS,
        'permiso_clave_COA': permiso_clave_COA,
        'permiso_clave_COG': permiso_clave_COG,
    }
    return render(request, 'main_app_data_basic.html', context)


@login_required
def generate_COG_key(request, arbitraje_id):
    arbitraje = get_object_or_404(Sistema_asovac,id=arbitraje_id)
    random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    random_password += 'COG'
    arbitraje.clave_maestra_coordinador_general = random_password
    arbitraje.save()
    messages.success(request, 'La contraseña de coordinador general ha sido generada.')

    usuario_rol_in_sistema = Usuario_rol_in_sistema.objects.filter(sistema_asovac_id = arbitraje.id, rol_id__in=[1, 2])

    nombre_sistema = Sistema_asovac.objects.get(id=request.session['arbitraje_id']).nombre
    nombre_rol = Rol.objects.get(id=2).nombre
    context = {
        'rol': nombre_rol,
        'sistema': nombre_sistema,
        'password': random_password,
        'arbitraje': arbitraje,
    }
    msg_plain = render_to_string('../templates/email_templates/password_generator.txt', context)
    msg_html = render_to_string('../templates/email_templates/password_generator.html', context)

    for item in usuario_rol_in_sistema:
        send_mail(
            'Asignación de contraseña',         #titulo
            msg_plain,                          #mensaje txt
            config('EMAIL_HOST_USER'),          #email de envio
            [item.usuario_asovac.usuario.email],               #destinatario
            html_message=msg_html,              #mensaje en html
        )

    return redirect('main_app:data_basic', arbitraje_id=arbitraje_id)

@login_required
def generate_COA_key(request, arbitraje_id):
    arbitraje = get_object_or_404(Sistema_asovac,id=arbitraje_id)
    random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    random_password += 'COA'
    arbitraje.clave_maestra_coordinador_area = random_password
    arbitraje.save()
    messages.success(request, 'La contraseña de coordinador de area ha sido generada.')

    usuario_rol_in_sistema = Usuario_rol_in_sistema.objects.filter(sistema_asovac_id = arbitraje.id, rol_id__in=[1, 3])

    nombre_sistema = Sistema_asovac.objects.get(id=request.session['arbitraje_id']).nombre
    nombre_rol = Rol.objects.get(id=3).nombre
    context = {
        'rol': nombre_rol,
        'sistema': nombre_sistema,
        'password': random_password,
        'arbitraje': arbitraje,
    }
    msg_plain = render_to_string('../templates/email_templates/password_generator.txt', context)
    msg_html = render_to_string('../templates/email_templates/password_generator.html', context)

    for item in usuario_rol_in_sistema:
        send_mail(
            'Asignación de contraseña',         #titulo
            msg_plain,                          #mensaje txt
            config('EMAIL_HOST_USER'),          #email de envio
            [item.usuario_asovac.usuario.email],               #destinatario
            html_message=msg_html,              #mensaje en html
        )
    return redirect('main_app:data_basic', arbitraje_id=arbitraje_id)

@login_required
def generate_ARS_key(request, arbitraje_id):
    arbitraje = get_object_or_404(Sistema_asovac,id=arbitraje_id)
    random_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
    random_password += 'ARS'
    arbitraje.clave_maestra_arbitro_subarea = random_password
    arbitraje.save()
    messages.success(request, 'La contraseña de arbitro de subarea ha sido generada.')

    usuario_rol_in_sistema = Usuario_rol_in_sistema.objects.filter(sistema_asovac_id = arbitraje.id, rol_id__in=[1, 4])

    nombre_sistema = Sistema_asovac.objects.get(id=request.session['arbitraje_id']).nombre
    nombre_rol = Rol.objects.get(id=4).nombre
    context = {
        'rol': nombre_rol,
        'sistema': nombre_sistema,
        'password': random_password,
        'arbitraje': arbitraje,
    }
    msg_plain = render_to_string('../templates/email_templates/password_generator.txt', context)
    msg_html = render_to_string('../templates/email_templates/password_generator.html', context)

    for item in usuario_rol_in_sistema:
        send_mail(
            'Asignación de contraseña',         #titulo
            msg_plain,                          #mensaje txt
            config('EMAIL_HOST_USER'),          #email de envio
            [item.usuario_asovac.usuario.email],               #destinatario
            html_message=msg_html,              #mensaje en html
        )
    return redirect('main_app:data_basic', arbitraje_id=arbitraje_id)

@login_required
def state_arbitration(request, arbitraje_id):
    # print (rol_id)
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    user_id = request.user.id
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf = get_route_configuracion(estado,rol_id, arbitraje_id)
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
            state = form.save()
            #Codigo para enviar correo electronico
            if state.estado_arbitraje == 8:
                autores_principal_list = Autores_trabajos.objects.filter(sistema_asovac = arbitraje, es_autor_principal = True, pagado = True)
                for autor_trabajo_principal in autores_principal_list:  
                    fecha = date.today()
                    autores_list = Autores_trabajos.objects.filter(trabajo = autor_trabajo_principal.trabajo)
                    context = {
                        'autor_trabajo_principal': autor_trabajo_principal,
                        'autores_list': autores_list,
                        'fecha': fecha,
                        'arbitraje': arbitraje,
                    }
                    if autor_trabajo_principal.trabajo.estatus == "Aceptado":
                        titulo = 'Carta de aceptación'
                        msg_plain = render_to_string('../templates/email_templates/carta_aceptacion.txt', context)
                        msg_html = render_to_string('../templates/email_templates/carta_aceptacion.html', context)
                    else:
                        titulo = 'Carta de rechazo'
                        msg_plain = render_to_string('../templates/email_templates/carta_rechazo.txt', context)
                        msg_html = render_to_string('../templates/email_templates/carta_rechazo.html', context)
                    
                    send_mail(
                            titulo,         #titulo
                            msg_plain,                          #mensaje txt
                            config('EMAIL_HOST_USER'),          #email de envio
                            [autor_trabajo_principal.autor.correo_electronico],               #destinatario
                            html_message=msg_html,              #mensaje en html
                            )
                
        else:
            print (form.errors)
        #estado = request.POST['estadoArbitraje']
        #print(estado)
        #request.session['estado'] = update_state_arbitration(arbitraje_id,estado)


    # si entro en el post se actualiza el estado de lo contrario no cambia y se lo paso a la vista igualmente        
    estado = request.session['estado']
    context = {
        'nombre_vista' : 'Cambiar Estado del Arbitraje',
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



@login_required
def users_list(request, arbitraje_id):
    rol_id = get_roles(request.user.id,arbitraje_id)
    users = User.objects.all()
    
    # rol = Usuario_asovac.objects.get(usuario_id=user.id).rol.all()
    user_asovac = Usuario_asovac.objects.all()
    users = Usuario_asovac.objects.all()
    print users
    for user in user_asovac:
        query = user.usuario.username
        # user.rol.all()
        # for rol in user.rol.all():
        #user.area_id.all()
        #print (query)

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje

    item_active = 1
    items = validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf = get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg = get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items

    context = {
        'nombre_vista' : 'Listado de Usuarios',
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



@login_required
def user_edit(request, arbitraje_id):
    rol_id=get_roles(request.user.id)

    # print (rol_id)
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
    # print items

    context = {
        'nombre_vista' : 'Editar Usuario',
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



@login_required
def user_roles(request, arbitraje_id):
    # print (rol_id)
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items

    context = {
        'nombre_vista' : 'Roles de los Usuarios',
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



@login_required
def coord_general(request, arbitraje_id):
    # print (rol_id)
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

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
        'nombre_vista' : 'Asignar Coordinador General',
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



@login_required
def coord_area(request, arbitraje_id):

    # print (rol_id)
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
    
    # print items

    context = {
        'nombre_vista' : 'Asignar Coordinador de Área',
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



@login_required
def total(request, arbitraje_id):

    # print (rol_id)
    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)
    
    item_active = 3
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items

    context = {
        'nombre_vista' : 'Total',
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



@login_required
def apps_selection(request):
    user_id= request.user.id
    data= dict()
    user= get_object_or_404(User,id=user_id)
    user= Usuario_asovac.objects.get(usuario_id=user_id)
    #user_role = user.biggest_role()

    try: 
        autor = Autor.objects.get(usuario = user)
        is_autor = True
    except:
        is_autor = False
    context = {
        #'user_role': user_role,
        'nombre_vista' : 'Selección de Aplicación',
        'user': user,
        'is_autor': is_autor
    }

    return render(request, 'main_app_aplicaciones_opc.html',context)



# Ajax/para el uso de ventanas modales
@login_required
def create_autor_instance_modal(request, user_id):
    data = dict()
    form = AuthorCreateAutorForm()
    if request.method == 'POST':
        form = AuthorCreateAutorForm(request.POST)
        universidad = request.POST.get("university_select") #Se colocó el valor de -1 para añadir una nueva universidad
        if form.is_valid():
            try:
                autor = form.save(commit = False)
                user = User.objects.get(id = user_id)
                usuario_asovac = Usuario_asovac.objects.get(usuario = user)
                autor.usuario = usuario_asovac
                autor.nombres = user.first_name
                autor.apellidos = user.last_name
                autor.correo_electronico = user.email
                if universidad != '-1':
                    autor.universidad = Universidad.objects.get(id = universidad)
                    autor.save()
                    request.session['is_author_created'] = True
                    data['url'] = reverse('trabajos:trabajos')
                    request.session['is_author_created'] = True  
                else:
                    data['url'] = reverse('autores:create_university_modal')
                    request.session['autor'] = serializers.serialize('json', [ autor, ])
                    data['reload_modal'] = True
                data['form_is_valid']= True           
            except:
                pass
    universidades = Universidad.objects.all()
    context = {
        'form':form,
        'universidades': universidades
    }
    data['html_form'] = render_to_string('ajax/author_create_autor_modal.html', context, request = request)
    return JsonResponse(data)



@login_required
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



@login_required
def create_user_modal(request):
    if request.method == 'POST':
        form= RegisterForm(request.POST)
    else:
        form= RegisterForm()

    return process_modal(request,form,'ajax/users-create.html')



@login_required
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



@login_required
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



@login_required
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



@login_required
def validate_access_modal(request,id):
    data= dict()
    user_id= request.user.id
    user= get_object_or_404(Usuario_asovac,usuario_id=user_id)
    arbitraje_id= id 
    # print "Arbitraje:",arbitraje_id

    if request.method == 'POST':
        print "El metodo es post"
        clave=request.POST['password']
        rol=request.POST['rol']
        data_arbitraje=Sistema_asovac.objects.get(pk=arbitraje_id) 
        # print "El rol es: ", request.POST['rol'], " El arbitraje es: ",data_arbitraje
        # print "Validate acces is: ",validate_access(rol,data_arbitraje,clave)
        if validate_access(rol,data_arbitraje,clave) == 1:
            params_validations= create_params_validations(request,1)
            data['form_is_valid']= True
            data['method']= 'post'
            # para enviar area a la cual pertenece el usuari por sesion 
            subareas= user.sub_area.all()
            # area y subarea a enviar por sesion 
            area_session=subareas.first().area.nombre
            subarea_session=subareas.first().nombre
            # print "Area y Subarea enviadas por sesion"
            # print area_session
            # print subarea_session
          
            request.session['area']= area_session
            request.session['subarea']=subarea_session

            context = {
                'params_validations' : params_validations,
                'arbitraje_id' : arbitraje_id,
            }
            data['html_form']= render_to_string('ajax/validate_rol_success.html',context,request=request)
        else:
            params_validations= create_params_validations(request,0)
            data['form_is_valid']= False
            data['method']= 'post'
            context = {
                'params_validations' : params_validations,
                'arbitraje_id' : arbitraje_id,
            }
            data['html_form']= render_to_string('ajax/validate_rol.html',context,request=request)
            
    else:
        # print "El metodo es get"
    
        params_validations= create_params_validations(request,2)
        data['form_is_valid']= True
        data['method']= 'get'
        context = {
            'params_validations' : params_validations,
            'arbitraje_id' : arbitraje_id,
        }
        data['html_form']= render_to_string('ajax/validate_rol.html',context,request=request)

    return JsonResponse(data)



#---------------------------------------------------------------------------------#
#                 Obtener lista de subareas asociadas a un area                   #
#---------------------------------------------------------------------------------#
def get_subareas(request,id):
    data= dict()

    subareas=Sub_area.objects.filter(area_id=id)
    context={'subareas': subareas,}
    data['html_select']= render_to_string('ajax/show_subareas.html',context, request=request)
    
    return JsonResponse(data)



#---------------------------------------------------------------------------------#
#                   Obtener Área asociada a un usuario                            #
#---------------------------------------------------------------------------------#
def get_area(user_id):
    usuario_asovac= Usuario_asovac.objects.get(usuario_id=user_id)
    area=0
    subarea=usuario_asovac.sub_area.first()
    # subarea=usuario_asovac.sub_area.get()
    area= subarea.area
    return area



#---------------------------------------------------------------------------------#
#                              Vista areas subareas                               #
#---------------------------------------------------------------------------------#
@login_required
def areas_subareas(request):

    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 1
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items

    context = {
        'nombre_vista' : 'Áreas y Subáreas',
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
    return render(request, 'main_app_areas_subareas.html', context)



#---------------------------------------------------------------------------------#
#                            Procesar carga de areas                              #
#---------------------------------------------------------------------------------#
@login_required
def process_areas_modal(request,form,template_name):
    data= dict()
    if request.method == 'POST':
        # if form.is_valid():
        status=200
        print "Se envia el archivo en post"
        if request.FILES != {}:
            data['form_is_valid']= True
            status=200
            response="Las áreas se han cargado de forma exitosa."
            data['message']= "Las áreas se han cargado de forma exitosa."
            try:
                request.FILES['file'].save_to_database(
                # name_columns_by_row=2,
                model=Area,
                mapdict=['nombre', 'descripcion','codigo'])
            except:
                print("Hay un error en los valores de entrada")
                data['form_is_valid']= False
                data['message']= "Ha ocurrido un error, verifique que los valores suministrados son validos."
                status=500
                response="Ha ocurrido un error, verifique que los valores suministrados son validos."

            context={
                'title': "Cargar Áreas",
                'response': response,
                'status': status,
            }
            data['html_form']= render_to_string(template_name,context, request=request)
            return JsonResponse(data) 

        else:
            data['form_is_valid']= False
  
    context={
        'form': form
    }
    data['html_form']= render_to_string(template_name,context, request=request)
    return JsonResponse(data) 



#---------------------------------------------------------------------------------#
#                          Procesar carga de subareas                             #
#---------------------------------------------------------------------------------#
@login_required
def process_subareas_modal(request,form,template_name):
    data= dict()
    if request.method == 'POST':
        # if form.is_valid():
        status=0
        if request.FILES != {}:
            data['form_is_valid']= True
            data['message']= "Las subáreas se han cargado de forma exitosa."
            status=1
            response="Las subáreas se han cargado de forma exitosa."
            try:
                request.FILES['file'].save_to_database(
                # name_columns_by_row=2,
                model=Sub_area,
                mapdict=['nombre', 'descripcion','area_id','codigo'])
            except:
                print("Hay un error en los valores de entrada")
                data['form_is_valid']= False
                status=0
                data['message']="Ha ocurrido un error, verifique que las áreas asignadas existen."
                response="Ha ocurrido un error, verifique que las áreas asignadas existen."
            
            context={
                'title': "Cargar Subáreas",
                'response': response,
                'status': status,
            }
            data['html_form']= render_to_string(template_name,context, request=request)
            return JsonResponse(data) 

        else:
            data['form_is_valid']= False
  
    context={
        'form': form
    }
    data['html_form']= render_to_string(template_name,context, request=request)
    return JsonResponse(data) 



#---------------------------------------------------------------------------------#
#                            Carga de areas via files                             #
#---------------------------------------------------------------------------------#
@login_required
def load_areas_modal(request):
    if request.method == 'POST':
        print 'el metodo es post'
        form= UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print request.FILES
            return process_areas_modal(request,form,'ajax/modal_succes.html')
        else:
            form= UploadFileForm(request.POST, request.FILES)
            return process_areas_modal(request,form,'ajax/load_areas.html')
    else:
        print 'el metodo es get'
        form= UploadFileForm()

    return process_areas_modal(request,form,'ajax/load_areas.html')



#---------------------------------------------------------------------------------#
#                          Carga de subareas via files                            #
#---------------------------------------------------------------------------------#
@login_required
def load_subareas_modal(request):
    if request.method == 'POST':
        print 'el metodo es post'
        form= UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print request.FILES
            return process_subareas_modal(request,form,'ajax/modal_succes.html')
        else:
            form= UploadFileForm(request.POST, request.FILES)
            return process_subareas_modal(request,form,'ajax/load_subareas.html')
    else:
        print 'el metodo es get'
        form= UploadFileForm()

    return process_subareas_modal(request,form,'ajax/load_subareas.html')



#---------------------------------------------------------------------------------#
#                            Carga de usuarios via files                          #
#---------------------------------------------------------------------------------#
@login_required
def load_users_modal(request,arbitraje_id,rol):
    data=dict()

    if request.method == 'POST':
        print 'el metodo es post'
        form= UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            # Para guardar el archivo de forma local
            file_name= save_file(request,"usuarios")
            extension= get_extension_file(file_name)

            #Valida el contenido del archivo 
            response= validate_load_users(file_name, extension,arbitraje_id,rol)
            print response

            context={
                'title': "Cargar Usuarios",
                'response': response['message'],
                'status': response['status'],
            }

            data['html_form']= render_to_string('ajax/modal_succes.html',context, request=request)
            return JsonResponse(data) 
        else:
            form= UploadFileForm(request.POST, request.FILES)
            context={
            'form': form,
            'arbitraje_id': arbitraje_id,
            'rol': rol,
            }
            data['html_form']= render_to_string('ajax/load_users.html',context, request=request)
            return JsonResponse(data) 
    else:
        print 'el metodo es get'
        form= UploadFileForm()

        context={
            'form': form,
            'arbitraje_id': arbitraje_id,
            'rol': rol,
        }
        data['html_form']= render_to_string('ajax/load_users.html',context, request=request)
        return JsonResponse(data) 



#---------------------------------------------------------------------------------#
#                Valida el contenido del excel para cargar usuarios               #
#---------------------------------------------------------------------------------#
def validate_load_users(filename,extension,arbitraje_id,rol):
    data= dict()
    data['status']=400
    data['message']="La estructura del archivo no es correcta"

    if extension == "xlsx" or extension == "xls":
        print "Formato xls/xlsx"
        book = xlrd.open_workbook(filename)   

        if book.nsheets > 0:
         
            print "El numero de hojas es mayor a 0 "
            sh = book.sheet_by_index(0)

            if sh.ncols == 17:
                print "El archivo tiene 17 columnas"
                data['status']=200
                data['message']="Se cargaron los usuarios de manera exitosa"

                # se validan los campos del documento
                for fila in range(sh.nrows):
                    # Para no buscar los titulos 
                    if fila > 0: 
                        # Se verifica si el correo electronico ya se encuentra registrado
                        email_exist=exist_email(sh.cell_value(rowx=fila, colx=3).strip())
                        email_count=count_email(sh,sh.cell_value(rowx=fila, colx=3).strip())
                        
                        # Se verifica que el campo nombre no este vacio
                        if sh.cell_value(rowx=fila, colx=0) == '':
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} el nombre es un campo obligatorio".format(fila)
                            break

                        # Se verifica que el campo apellido no este vacio
                        if sh.cell_value(rowx=fila, colx=1) == '':
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} el apellido es un campo obligatorio".format(fila)
                            break

                        # Se verifica que el campo nombre de usuario no este vacio
                        if sh.cell_value(rowx=fila, colx=2) == '':
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} el nombre de usuario es un campo obligatorio".format(fila)
                            break

                        # Se verifica que el campo correo electronico no este vacio
                        if sh.cell_value(rowx=fila, colx=3) == '':
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} el correo es un campo obligatorio".format(fila)
                            break
                        
                        # Se verifica que el campo genero no este vacio
                        if sh.cell_value(rowx=fila, colx=8) == '':
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} el genero es un campo obligatorio".format(fila)
                            break

                        # Se verifica que el campo cedula o pasaporte no este vacio
                        if sh.cell_value(rowx=fila, colx=9) == '':
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} la cédula o pasaporte es un campo obligatorio".format(fila)
                            break

                        # Se verifica que el campo titulo no este vacio
                        if sh.cell_value(rowx=fila, colx=10) == '':
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} el titulo es un campo obligatorio".format(fila)
                            break

                        # Se verifica que el campo linea de investigación no este vacio
                        if sh.cell_value(rowx=fila, colx=11) == '':
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} la linea de investigación es un campo obligatorio".format(fila)
                            break

                        # Se verifica que el campo celular no este vacio
                        if sh.cell_value(rowx=fila, colx=13) == '':
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} el teléfono celular o habitación es un campo obligatorio".format(fila)
                            break
                        
                        # Se verifica que el campo correo electronico sea unico
                        if email_count > 1:
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} el correo {1} debe ser asignado a un solo usuario".format(fila,sh.cell_value(rowx=fila, colx=3))
                            break

                        # Se verifica que el campo correo electronico sea unico
                        if email_exist == True:
                            # print "Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            data['status']=400
                            data['message']="Error en la fila {0} el correo {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=3))
                            break

                        # Se verifica si el username ya se encuentra registrado
                        username_exist=exist_username(sh.cell_value(rowx=fila, colx=2).strip())
                        username_count=count_username(sh,sh.cell_value(rowx=fila, colx=2).strip())

                        if username_count > 1:
                            # print "Error en la fila {0} el usuario {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=2))
                            data['status']=400
                            data['message']="Error en la fila {0} el nombre de usuario {1} debe ser asignado a un solo usuario".format(fila,sh.cell_value(rowx=fila, colx=2))
                            break

                        if username_exist == True:
                            # print "Error en la fila {0} el usuario {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=2))
                            data['status']=400
                            data['message']="Error en la fila {0} el usuario {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=2))
                            break

                        # Se verifica si el area ya se encuentra registrada
                        area_exist=exist_area(sh.cell_value(rowx=fila, colx=4).strip())
                        if area_exist == False:
                            # print "Error en la fila {0} el usuario {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=2))
                            data['status']=400
                            data['message']="Error en la fila {0} el área {1} no se encuentra registrada".format(fila,sh.cell_value(rowx=fila, colx=4))
                            break

                         # Se verifica si el area ya se encuentra registrada
                        subarea1_exist=""
                        subarea2_exist=""
                        subarea3_exist=""

                        if sh.cell_value(rowx=fila, colx=5) != "": 
                            subarea1_exist=exist_subarea(sh.cell_value(rowx=fila, colx=4),sh.cell_value(rowx=fila, colx=5).strip())

                        if sh.cell_value(rowx=fila, colx=6) != "":
                            subarea2_exist=exist_subarea(sh.cell_value(rowx=fila, colx=4),sh.cell_value(rowx=fila, colx=6).strip())

                        if sh.cell_value(rowx=fila, colx=7) != "":
                            subarea3_exist=exist_subarea(sh.cell_value(rowx=fila, colx=4),sh.cell_value(rowx=fila, colx=7).strip())

                        if subarea1_exist == "" and subarea2_exist == "" and subarea3_exist == "":
                            data['status']=400
                            data['message']="Error en la fila {0}  debe registrar almenos 1 subárea. ".format(fila)
                            break

                        if subarea1_exist == False:
                            # print "Error en la fila {0} el usuario {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=2))
                            data['status']=400
                            data['message']="Error en la fila {0} la subárea1 '{1}' no se encuentra registrada en el área {2}".format(fila,sh.cell_value(rowx=fila, colx=5),sh.cell_value(rowx=fila, colx=4))
                            break

                        if subarea2_exist == False:
                            # print "Error en la fila {0} el usuario {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=2))
                            data['status']=400
                            data['message']="Error en la fila {0} la subárea2 '{1}' no se encuentra registrada en el área {2}".format(fila,sh.cell_value(rowx=fila, colx=6),sh.cell_value(rowx=fila, colx=4))
                            break
                        
                        if subarea3_exist == False:
                            # print "Error en la fila {0} el usuario {1} ya se encuentra registrado".format(fila,sh.cell_value(rowx=fila, colx=2))
                            data['status']=400
                            data['message']="Error en la fila {0} la subárea3 '{1}' no se encuentra registrada en el área {2}".format(fila,sh.cell_value(rowx=fila, colx=7),sh.cell_value(rowx=fila, colx=4))
                            break

                # Inserta los registros una vez realizada la validación correspondiente
                if data['status'] == 200:
                    is_create=create_users(sh,arbitraje_id,rol)
                    print is_create
                    if is_create == 400:
                        data['status']=400
                        data['message']="Ha ocurrido un error, los datos no fueron cargado de forma correcta."
                    print "Los datos del archivo son válidos"

    return data 



#---------------------------------------------------------------------------------#
#             Verifica si existe el correo o el nombre de usuario                 #
#---------------------------------------------------------------------------------#
def exist_email(email):
    exist= User.objects.filter(email=email).exists()
    return exist



def exist_username(user):
    exist= User.objects.filter(username=user).exists()
    return exist



def exist_area(area):
    exist= Area.objects.filter(nombre=area).exists()
    return exist



def exist_subarea(area, subarea):
    # print subarea
    query= Area.objects.get(nombre=area)
    exist= Sub_area.objects.filter(nombre=subarea,area_id=query.id).exists()
    
    return exist



def count_email(sh,email):
    cont=0
    for fila in range(sh.nrows):
        if email== sh.cell_value(rowx=fila, colx=3):
            cont=cont+1
    return cont



def count_username(sh,username):
    cont=0
    for fila in range(sh.nrows):
        if username== sh.cell_value(rowx=fila, colx=2):
            cont=cont+1
        # print "El contador vale: ",cont
    return cont



def create_users(sh,arbitraje_id,rol):
    for fila in range(sh.nrows):
        if fila > 0: 
            # Guarda el usuario
            try: 
                user= User()
                user.first_name=sh.cell_value(rowx=fila, colx=0).strip()
                user.last_name=sh.cell_value(rowx=fila, colx=1).strip()
                user.username=sh.cell_value(rowx=fila, colx=2).strip()
                user.email=sh.cell_value(rowx=fila, colx=3).strip()
                clave= get_random_string(length=12)
                user.password=make_password(clave)
                user.save()
                # print "Se crea el usuario: ", user.first_name

                # Guarda la subarea
                usuario_asovac= Usuario_asovac.objects.get(usuario=user)
                arbitraje=Sistema_asovac.objects.get(id=arbitraje_id)

                if sh.cell_value(rowx=fila, colx=5) != "":
                    # calcular el id de cada subarea para mandarlo por parametro
                    # print "subarea 1"
                    subarea_id= get_subarea(sh.cell_value(rowx=fila, colx=5).strip())
                    usuario_asovac.sub_area.add(Sub_area.objects.get(id=subarea_id))
                    usuario_asovac.save()
                
                if sh.cell_value(rowx=fila, colx=6) != "":
                    # calcular el id de cada subarea para mandarlo por parametro
                    # print "subarea 2"
                    subarea_id= get_subarea(sh.cell_value(rowx=fila, colx=6).strip())
                    usuario_asovac.sub_area.add(Sub_area.objects.get(id=subarea_id))
                    usuario_asovac.save()
                
                if sh.cell_value(rowx=fila, colx=7) != "":
                    # calcular el id de cada subarea para mandarlo por parametro
                    # print "subarea 3"
                    subarea_id= get_subarea(sh.cell_value(rowx=fila, colx=7).strip())
                    usuario_asovac.sub_area.add(Sub_area.objects.get(id=subarea_id))
                    usuario_asovac.save()

                # Guarda el rol asociado al sistema donde se esta cargando el usuario 
                itemRole= Rol.objects.get(id=rol)
                # Se construye el objeto para crear los roles
                addRol=Usuario_rol_in_sistema()
                addRol.usuario_asovac=usuario_asovac
                addRol.rol=itemRole
                addRol.sistema_asovac=arbitraje
                addRol.save()

                # Guarda los datos asociados al arbitro
                
                # Campos obliogatorios
                arbitro =Arbitro()
                arbitro.nombres=sh.cell_value(rowx=fila, colx=0).strip()
                arbitro.apellidos=sh.cell_value(rowx=fila, colx=1).strip()
                arbitro.genero=sh.cell_value(rowx=fila, colx=8).strip()
                arbitro.cedula_pasaporte=str(sh.cell_value(rowx=fila, colx=9)).replace(".0","").strip()
                arbitro.titulo=sh.cell_value(rowx=fila, colx=10).strip()
                arbitro.linea_investigacion=sh.cell_value(rowx=fila, colx=11).strip()
                arbitro.telefono_habitacion_celular=str(sh.cell_value(rowx=fila, colx=13)).replace(".0","").strip()
                arbitro.correo_electronico=user.email
                arbitro.usuario=usuario_asovac

                # Campos opcionales
                if sh.cell_value(rowx=fila, colx=12) != "":
                    arbitro.telefono_oficina=str(sh.cell_value(rowx=fila, colx=12)).replace(".0","").strip()
                if sh.cell_value(rowx=fila, colx=13) != "":
                    arbitro.institucion_trabajo=sh.cell_value(rowx=fila, colx=14).strip()
                if sh.cell_value(rowx=fila, colx=14) != "":
                    arbitro.datos_institucion=sh.cell_value(rowx=fila, colx=15).strip()
                if sh.cell_value(rowx=fila, colx=15) != "":
                    arbitro.observaciones=sh.cell_value(rowx=fila, colx=16).strip()
                if(rol == "4"):
                    # Coordinador de área
                    arbitro.save()
                    arbitro.Sistema_asovac.add(arbitraje)
                    arbitro.save()
                    clave_arbitraje= arbitraje.clave_maestra_arbitro_subarea
                    clave_arbitraje_rol="Árbitro de Subárea"
                    # print clave_arbitraje
                    # Envío de correo
                    context = {
                        'clave_arbitraje_rol':clave_arbitraje_rol,
                        'clave_arbitraje':clave_arbitraje,
                        'username': user.username ,
                        'password':clave,
                        'nombre':user.first_name,
                        'apellido':user.last_name,
                        'arbitraje': arbitraje,
                    }
                    msg_plain = render_to_string('../templates/email_templates/create_user.txt', context)
                    msg_html = render_to_string('../templates/email_templates/create_user.html', context)

                    send_mail(
                        'Registro de usuario',              #titulo
                        msg_plain,                          #mensaje txt
                        config('EMAIL_HOST_USER'),          #email de envio
                        [user.email],                       #destinatario
                        html_message=msg_html,              #mensaje en html
                        )
                else:
                    # Árbitro de Subárea
                    arbitro.save()
                    clave_arbitraje= arbitraje.clave_maestra_coordinador_area
                    clave_arbitraje_rol="Coordinador de Área"
                    print clave_arbitraje
                    # Envío de correo
                    context = {
                        'clave_arbitraje_rol':clave_arbitraje_rol,
                        'clave_arbitraje':clave_arbitraje,
                        'username': user.username ,
                        'password':clave,
                        'nombre':user.first_name,
                        'apellido':user.last_name,
                        'arbitraje': arbitraje,
                    }
                    msg_plain = render_to_string('../templates/email_templates/create_user.txt', context)
                    msg_html = render_to_string('../templates/email_templates/create_user.html', context)

                    send_mail(
                        'Registro de usuario',              #titulo
                        msg_plain,                          #mensaje txt
                        config('EMAIL_HOST_USER'),          #email de envio
                        [user.email],                       #destinatario
                        html_message=msg_html,              #mensaje en html
                        )
            except:
                print "Ha ocurrido un error con los parametros recibidos"   
                return 400
    return 200 



#---------------------------------------------------------------------------------#
#                 Para obtener el id de la subarea importada                      #
#---------------------------------------------------------------------------------#
def get_subarea(name):
    # print "Area a crear: ",name
    subarea=Sub_area.objects.get(nombre=name)
    return subarea.id



#---------------------------------------------------------------------------------#
#                Guarda el archivo en la carpeta del proyecto                     #
#---------------------------------------------------------------------------------#
def handle_uploaded_file(file, filename):
    if not os.path.exists('upload/'):
        os.mkdir('upload/')

    # print "Nombre del archivo a guardar: ",filename
    with open('upload/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)



#---------------------------------------------------------------------------------#
#                   Carga el contenido de la tabla de areas                       #
#---------------------------------------------------------------------------------#
@login_required
def list (request):
    response = {}
    response['query'] = []

    sort= request.POST['sort']
    search= request.POST['search']
    # Se verifica la existencia del parametro
    if request.POST.get('offset', False) != False:
        init= int(request.POST['offset'])
    
    # Se verifica la existencia del parametro
    if request.POST.get('limit', False) != False:
        limit= int(request.POST['limit'])+init
    
    # init= int(request.POST['offset'])
    # limit= int(request.POST['limit'])+init
    # print "init: ",init,"limit: ",limit

    if request.POST['order'] == 'asc':
        if sort == 'fields.nombre':
            order='nombre'
        else:
            if sort == 'fields.descripcion':
                order='descripcion'
            else:
                order=sort
    else:
        if sort == 'fields.nombre':
            order='-nombre'
        else:
            if sort == 'fields.descripcion':
                order='-descripcion'
            else:
                order='-'+sort

    if search != "":
        data=Area.objects.all().filter( Q(pk__contains=search) | Q(nombre__contains=search) | Q(descripcion__contains=search) | Q(codigo__contains=search) ).order_by(order)#[:limit]
        total= len(data)
    else:
        if request.POST.get('limit', False) == False or request.POST.get('offset', False) == False:
            print "consulta para exportar"
            print Area.objects.all().order_by(order).query
            data=Area.objects.all().order_by(order)
            total= Area.objects.all().count()
        else:
            print "consulta normal"
            # print Area.objects.all().order_by(order)[init:limit].query
            test= Sub_area.objects.all().order_by(order)[init:limit]
            data=Area.objects.all().order_by(order)[init:limit]
            total= Area.objects.all().count()
            # test=Area.objects.raw('SELECT a.*, (SELECT count(area.id) FROM main_app_area as area) FROM main_app_area as a LIMIT %s OFFSET %s',[limit,init])
    # response['total']=total
    # print response
    for item in data:
        # print("%s is %s. and total is %s" % (item.nombre, item.descripcion,item.count))
        response['query'].append({'id':item.pk,'nombre': item.nombre,'descripcion': item.descripcion,'codigo': item.codigo})

    response={
        'total': total,
        'query': response,
    }
   
    return JsonResponse(response)



#---------------------------------------------------------------------------------#
#                                   Crud Areas                                    #
#---------------------------------------------------------------------------------#
@login_required
def viewArea(request,id):
    data= dict()
    area=Area.objects.get(id=id)
    data['status']= 200
    context={
        'area':area,
        'tipo':"show"
    }
    data['content']= render_to_string('ajax/BTArea.html',context,request=request)
    return JsonResponse(data)



@login_required
def editArea(request,id):
    data= dict()

    if request.method == 'POST':
        
        area=Area.objects.get(id=id)
        # print "edit post"
        form= AreaCreateForm(request.POST,instance=area)
        if form.is_valid():
            # print "Se guarda el valor del formulario"
            form.save()
            data['status']= 200
            data['message']= "Se ha actualizado el área de forma exitosa."
        else:
            data['status']= 404
            data['message']= "Ha ocurrido un error, no se ha podido actualizar el área."
    else:
        area=Area.objects.get(id=id)
        data['status']= 200
        data['title']=area.nombre
        form=AreaCreateForm(instance=area)
        context={
            'area':area,
            'tipo':"edit",
            'form':form,
        }
        data['content']= render_to_string('ajax/BTArea.html',context,request=request)
    return JsonResponse(data)



@login_required
def removeArea(request,id):
    
    data= dict()

    if request.method == 'POST':
        print "post delete form"
        area=Area.objects.get(id=id)
        area.delete()
        data['status']= 200
        message="Se ha eliminado el área de forma exitosa."
        data['message']= message
        # context={
        #     'area':area,
        #     'tipo':"deleted",
        #     'message':message,
        # }
        # data['content']= render_to_string('ajax/BTArea.html',context,request=request)

    else:
        # print "get delete form"
        area=Area.objects.get(id=id)
        data['status']= 200
        data['title']=area.nombre
        form=AreaCreateForm(instance=area)
        message="eliminar"
        context={
            'area':area,
            'tipo':"delete",
            'form':form,
            'message':message,
        }
        data['content']= render_to_string('ajax/BTArea.html',context,request=request)
    return JsonResponse(data)



#---------------------------------------------------------------------------------#
#                  Carga el contenido de la tabla de Subareas                     #
#---------------------------------------------------------------------------------#
@login_required
def list_subareas(request):
    response = {}
    response['query'] = []

    sort= request.POST['sort']
    search= request.POST['search']
    # Se verifica la existencia del parametro
    if request.POST.get('offset', False) != False:
        init= int(request.POST['offset'])
    
    # Se verifica la existencia del parametro
    if request.POST.get('limit', False) != False:
        limit= int(request.POST['limit'])+init

    if request.POST['order'] == 'asc':
        if sort == 'fields.nombre':
            order='nombre'
        else:
            if sort == 'fields.descripcion':
                order='descripcion'
            else:
                order=sort
    else:
        if sort == 'fields.nombre':
            order='-nombre'
        else:
            if sort == 'fields.descripcion':
                order='-descripcion'
            else:
                order='-'+sort

    if search != "":
        data=Sub_area.objects.all().filter( Q(pk__contains=search) | Q(nombre__contains=search) | Q(descripcion__contains=search) | Q(codigo__contains=search) ).order_by(order)#[:limit]
        total= len(data)
    else:
        if request.POST.get('limit', False) == False or request.POST.get('offset', False) == False:
            print "consulta para exportar"
            print Sub_area.objects.all().order_by(order).query
            data=Sub_area.objects.all().order_by(order)
            total= Sub_area.objects.all().count()
        else:
            print "consulta normal"
            # print Sub_area.objects.all().order_by(order)[init:limit].query
            # test= Sub_area.objects.all().order_by(order)[init:limit]
            data=Sub_area.objects.all().order_by(order)[init:limit]
            total= Sub_area.objects.all().count()
            # test=Sub_area.objects.raw('SELECT a.*, (SELECT count(area.id) FROM main_app_area as area) FROM main_app_area as a LIMIT %s OFFSET %s',[limit,init])
    # response['total']=total
    # print response
    for item in data:
        # print("%s is %s. and total is %s" % (item.nombre, item.descripcion,item.count))
        response['query'].append({'id':item.pk,'nombre': item.nombre,'descripcion': item.descripcion,'codigo':item.codigo})

    response={
        'total': total,
        'query': response,
    }
   
    return JsonResponse(response)



#---------------------------------------------------------------------------------#
#                                 Crud Subareas                                   #
#---------------------------------------------------------------------------------#
@login_required
def viewSubarea(request,id):
    data= dict()
    subarea=Sub_area.objects.get(id=id)
    data['status']= 200
    context={
        'subarea':subarea,
        'tipo':"show"
    }
    data['content']= render_to_string('ajax/BTSubarea.html',context,request=request)
    return JsonResponse(data)



@login_required
def editSubarea(request,id):
    data= dict()
    if request.method == 'POST':
        
        subarea=Sub_area.objects.get(id=id)
        form= AreaCreateForm(request.POST,instance=subarea)
        if form.is_valid():
            print "Se guarda el valor del formulario"
            form.save()
            data['status']= 200
            data['message']= "Se ha actualizado la subárea de forma exitosa."
        else:
            data['status']= 404
            data['message']= "Ha ocurrido un error, no se ha podido actualizar la subárea."
    else:
        subarea=Sub_area.objects.get(id=id)
        data['status']= 200
        data['title']=subarea.nombre
        form=AreaCreateForm(instance=subarea)
        context={
            'subarea':subarea,
            'tipo':"edit",
            'form':form,
        }
        data['content']= render_to_string('ajax/BTSubarea.html',context,request=request)
    return JsonResponse(data)



@login_required
def removeSubarea(request,id):
    
    data= dict()

    if request.method == 'POST':
        print "post delete form"
        subarea=Sub_area.objects.get(id=id)
        subarea.delete()
        data['status']= 200
        data['message']="Se ha eliminado la subárea de forma exitosa."
        message="eliminado"
        context={
            'subarea':subarea,
            'tipo':"deleted",
            'message':message,
        }
        data['content']= render_to_string('ajax/BTSubarea.html',context,request=request)

    else:
        print "get delete form"
        subarea=Sub_area.objects.get(id=id)
        data['status']= 200
        data['title']=subarea.nombre
        form=AreaCreateForm(instance=subarea)
        message="eliminar"
        context={
            'subarea':subarea,
            'tipo':"delete",
            'form':form,
            'message':message,
        }
        data['content']= render_to_string('ajax/BTSubarea.html',context,request=request)
    return JsonResponse(data)



@login_required
def register_user_in_sistema(request, arbitraje_id):
    data = dict()
    if request.method == 'POST':
        usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
        arbitraje = Sistema_asovac.objects.get(id = arbitraje_id)
        rol = Rol.objects.get(id = 5)

        new_usuario_rol_in_sistema = Usuario_rol_in_sistema(rol = rol, sistema_asovac = arbitraje, usuario_asovac = usuario_asovac)
        new_usuario_rol_in_sistema.save()

        rol_id = get_roles(request.user.id , arbitraje.id)
        if (1 == rol_id) or (2 >= rol_id and arbitraje.estado_arbitraje != 0) or (3 >= rol_id and arbitraje.estado_arbitraje != 0) or (4 >= rol_id and arbitraje.estado_arbitraje in [5,6,8]) or (5 >= rol_id and arbitraje.estado_arbitraje in [3,6]):
            return redirect(reverse('main_app:dashboard', kwargs={'arbitraje_id':arbitraje.id}))
        else:
            messages.success(request, 'Se ha registrado en el sistema éxitosamente, debe esperar al estado del arbitraje "En carga de trabajos" para poder ingresar en la plataforma.')
            return redirect('main_app:home')
    else:
        arbitraje = Sistema_asovac.objects.get(id =arbitraje_id)
        context = {
            'arbitraje': arbitraje,
        }
        data['html_form'] = render_to_string('ajax/register_user_in_sistema.html', context, request = request)
    return JsonResponse(data)



@login_required
def changepassword_modal(request):
    data = dict()
    if request.method == 'POST':
        form = ChangePassForm(request.user, request.POST)
        if form.is_valid():
            try:
                form.save()
                update_session_auth_hash(request, form.user)

                #Envio de email con las nuevas credenciales al correo electrónico del usuario
                
                user = User.objects.get(pk=request.user.id)
                context = {
                    'username': user.username,
                    'password':form.cleaned_data['new_password1']
                }

                msg_plain = render_to_string('../templates/email_templates/changepassword.txt', context)
                msg_html = render_to_string('../templates/email_templates/changepassword.html', context)

                send_mail(
                        'Cambio de Contraseña - Asovac',      #titulo
                        msg_plain,                                  #mensaje txt
                        config('EMAIL_HOST_USER'),                        #email de envio
                        [user.email],                               #destinatario
                        html_message=msg_html,                      #mensaje en html
                        )

                # Nos aseguramos siempre de desbloquar a un usuario despues de el cambio de contraseña
                messages.success(request, 'Se ha cambiado su contraseña con éxito')
                data['form_is_valid']= True
            except:
                pass
    else:
        form = ChangePassForm(request.user)
    
    context = {
        'form': form,
    }
    data['html_form'] = render_to_string('ajax/changepassword_modal.html', context, request = request)
    
    return JsonResponse(data)



#---------------------------------------------------------------------------------#
#                  Carga el contenido de la tabla de usuarios                     #
#---------------------------------------------------------------------------------#
@login_required
def list_usuarios(request):
    
    response = {}
    response['query'] = []

    sort= request.POST['sort']
    order= request.POST['order']
    search= request.POST['search']
    
    # Se verifica la existencia del parametro
    if request.POST.get('offset', False) != False:
        init= int(request.POST['offset'])
    
    # Se verifica la existencia del parametro
    if request.POST.get('limit', False) != False:
        limit= int(request.POST['limit'])+init
    
    if request.POST.get('export',False) != False:
        export= request.POST.get('export')
    else:
        export= ""

    if sort == 'pk':
        sort='first_name'


    if search != "" and export == "":
        print "Consulta Search"
        # data= Usuario_asovac.objects.select_related('arbitro','usuario').filter( Q(usuario__username__contains=search) | Q(usuario__first_name__contains=search) | Q(usuario__last_name__contains=search) | Q(usuario__email__contains=search) ).order_by(order)
        # total= len(data)
        # data=User.objects.all().filter( Q(username__contains=search) | Q(first_name__contains=search) | Q(last_name__contains=search) | Q(email__contains=search) ).order_by(order)#[:limit]
        query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id"           
        query_count=query
        search= search+'%'
        where=' WHERE au.first_name like %s or au.last_name like %s or au.username like %s or au.email like %s '
        # where=' WHERE au.first_name LIKE %s' 
        query= query+where
        order_by="au."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
        # query= query + " ORDER BY " + order_by
        
        data= User.objects.raw(query,[search,search,search,search])
        data_count= User.objects.raw(query,[search,search,search,search])
        # data_count= User.objects.raw(query_count)
        total=0
        for item in data_count:
            total=total+1
    else:
        # if request.POST.get('limit', False) == False or request.POST.get('offset', False) == False:
        if export !=  "":
    
            print "Consulta para Exportar Todo"

        else:
            print "Consulta Normal"
            arbitraje_id = request.session['arbitraje_id']
            # consulta basica
            # data=User.objects.all().order_by(order)[init:limit].query
            # data=User.objects.all().order_by('pk')[init:limit].query

            # consulta mas completa
            query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id"           
            order_by="au."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
            query_count=query
            query= query + " ORDER BY " + order_by
            
            data= User.objects.raw(query)
            data_count= User.objects.raw(query_count)
            total=0
            for item in data_count:
                total=total+1
  
            # data= Usuario_asovac.objects.select_related('arbitro','usuario').filter( id=27).order_by(order)
            # total= len(data)

    # for item in data:
        # print("%s is %s. and total is %s" % (item.username, item.first_name,item.last_name, item.email))
        # response['query'].append({'id':item.id,'first_name': item.first_name,'last_name':item.last_name,'username': item.username,'email':item.email})
    
    for item in data:
        username= item.username 
        first_name= item.first_name 
        last_name= item.last_name 
        email= item.email 
        area= item.nombre 
        linea_investigacion= item.linea_investigacion 
        cedula_pasaporte=  item.cedula_pasaporte 
        titulo= item.titulo 
        response['query'].append({'id':item.id,'first_name': first_name ,'last_name':last_name ,'username':username ,'email':email  , 'nombre':area  , 'linea_investigacion':linea_investigacion , 'cedula_pasaporte':cedula_pasaporte,'titulo':titulo })


    response={
        'total': total,
        'query': response,
    }
   
    return JsonResponse(response)



#---------------------------------------------------------------------------------#
#                               Exportar Usuarios                                 #
#---------------------------------------------------------------------------------#
@login_required
def generate_report(request,tipo):

    # Para exportar información de usuarios 
    if tipo == '1':
        # consulta para obtener informacion de los usuarios
        query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id"
        query_count=query
        query= query
        
        data= User.objects.raw(query)
        data_count= User.objects.raw(query_count)
        total=0
        for item in data_count:
            total=total+1

        # Para definir propiedades del documento de excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Usuarios.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet("Usuarios")
        # Para agregar los titulos de cada columna
        row_num = 0
        columns = ['Nombres (*)', 'Apellidos (*)', 'Nombre de usuario (*)','Correo electronico (*)','Área (*)','Subarea 1 (*)','Subarea 2','Subarea 3','Género (*)','Cédula o pasaporte (*)','Título (*)','Línea de investigación (*)','Teléfono oficina','Teléfono celular o habitación (*)','Institución donde  trabaja','Datos de la institución','Observaciones']
        for col_num in range(len(columns)):
            worksheet.write(row_num, col_num, columns[col_num])     
        
        for item in data:
            row_num += 1
            row = [item.first_name ,item.last_name ,item.username ,item.email,item.nombre,'-','-','-','-',item.cedula_pasaporte,item.titulo,item.linea_investigacion,'-','-','-','-','-']
            for col_num in range(len(row)):
                worksheet.write(row_num, col_num, row[col_num])
        
        workbook.save(response)

    return response



#---------------------------------------------------------------------------------#
#                                 Crud Usuarios                                   #
#---------------------------------------------------------------------------------#
@login_required
def viewUsuario(request,id,arbitraje_id):
    data= dict()
    user=User.objects.get(id=id)
    data['status']= 200
    context={
        'user':user,
        'tipo':"show"
    }
    data['content']= render_to_string('ajax/BTUsuarios.html',context,request=request)
    return JsonResponse(data)



@login_required
def editUsuario(request,id,arbitraje_id):
    data= dict()
    user=  get_object_or_404(User,id=id)

    # Usuario seleccionado 
    # user_asovac= get_object_or_404(Usuario_asovac,usuario=id)
    user_asovac= Usuario_asovac.objects.get(usuario=id)
    user_role= get_roles(user.id,"is_admin")
    # print "Usuario seleccionado User: ", id," Arbitraje ",arbitraje_id
    rols= get_role_list(id,arbitraje_id)

    # Obtenemos el mayor rol del usuario que hizo la petición
    # request_user= get_object_or_404(Usuario_asovac,usuario_id=request.user.id)
    request_user= Usuario_asovac.objects.get(usuario=request.user.id)
    # print "Usuario autenticado User: ", request_user.id," Arbitraje ",arbitraje_id
    request_user_role= get_roles(request_user.id,"is_admin")

    if(request_user_role > user_role):
        permiso="rol-no-permitido"
    else:
        permiso="rol-permitido"

    if request.method == 'POST':
        
        # print "edit post"
        form= PerfilForm(request.POST,instance=user)
        if form.is_valid():
            print "Se guarda el valor del formulario"
            form.save()
            data['status']= 200
        else:
            data['status']= 404
    else:
       
        data['status']= 200
        data['title']=user.username
        form= PerfilForm(instance=user)
        context={
            'user':user,
            'arbitraje_id':arbitraje_id,
            'tipo':"edit",
            'form':form,
            'permiso':permiso,
        }
        data['content']= render_to_string('ajax/BTUsuarios.html',context,request=request)
    return JsonResponse(data)



@login_required
def removeUsuario(request,id,arbitraje_id):

    data= dict()

    # Usuario seleccionado 
    user_asovac= get_object_or_404(Usuario_asovac,usuario=id)
    user_role= get_roles(id,"is_admin")
    # print "Usuario seleccionado User: ", id," Arbitraje ",arbitraje_id
    rols= get_role_list(id,arbitraje_id)
    
    # Obtenemos el mayor rol del usuario que hizo la petición
    request_user= get_object_or_404(Usuario_asovac,usuario_id=request.user.id)
    request_user_role= get_roles(request_user.id,"is_admin")

    if(request_user_role > user_role):
        permiso="rol-no-permitido"
    else:
        permiso="rol-permitido"

    if request.method == 'POST':
        print "post delete form"
        user=get_object_or_404(User,id=id)
        user.delete()
        data['status']= 200
        message="eliminado"
        context={
            'user':user,
            'tipo':"deleted",
            'message':message,
        }
        data['content']= render_to_string('ajax/BTUsuarios.html',context,request=request)

    else:
        # print "get delete form"
        user=get_object_or_404(User,id=id)
        data['status']= 200
        data['title']=user.username
        form= PerfilForm(instance=user)
        message="eliminar"
        context={
            'user':user,
            'tipo':"delete",
            'arbitraje_id':arbitraje_id,
            'form':form,
            'permiso':permiso,
            'message':message,
        }
        data['content']= render_to_string('ajax/BTUsuarios.html',context,request=request)
    return JsonResponse(data)



@login_required
def changeRol(request,id,arbitraje_id):
    
    # Lista de roles
    rol_list=Rol.objects.all()
    array_rols=[]

    for item in rol_list:
        array_rols.append(item.id)
    
    # print "Array de roles: ",array_rols

    #datos del usuario y arbitraje 
    data=dict()
    user=User.objects.get(id=id)
    arbitraje=Sistema_asovac.objects.get(id=arbitraje_id)
    # Usuario seleccionado 
    user_asovac= get_object_or_404(Usuario_asovac,usuario=id)
    user_role= get_roles(id,"is_admin")
    # rols= get_role_list(user_asovac.id,arbitraje_id)
    rols= get_role_list(id,arbitraje_id)
    
    # Obtenemos el mayor rol del usuario que hizo la petición
    request_user= get_object_or_404(Usuario_asovac,usuario_id=request.user.id)
    request_user_role= get_roles(request_user.id,"is_admin")

    if request.method == 'POST':
        
        # print "update rol"
        form= AssingRolForm(request.POST) 
        params_rol=request.POST.getlist("rol")
        params_user=request.POST.getlist("usuario_asovac")
        params_arbitraje=request.POST.getlist("sistema_asovac")
        # print "Rol recibido: ",params_rol," Usuario: ",params_user," Arbitraje: ",params_arbitraje
        if form.is_valid():
            # print "Se guarda el valor del formulario"
            # Borrar registros anteriores para evitar repeticion de registros
            delete=Usuario_rol_in_sistema.objects.filter(sistema_asovac=arbitraje,usuario_asovac=user_asovac).delete()
            # Para verificar que el usuario tenga registro en la tabla de arbitros
            arbitro_exist=Arbitro.objects.filter(usuario=user_asovac).exists()
        
            if not arbitro_exist:
                # Para crear registro en la tabla arbitro de usuarios no cargados por excel y se le modifique el rol
                user_select= get_object_or_404(User,id=user_asovac.usuario_id)
                arbitro =Arbitro()
                arbitro.nombres=user_select.first_name
                arbitro.apellidos=user_select.last_name
                arbitro.correo_electronico=user_select.email
                arbitro.usuario=user_asovac
                arbitro.save()
            else:
                arbitro= get_object_or_404(Arbitro,usuario=user_asovac)
                arbitro.Sistema_asovac.remove(arbitraje)
            # print delete
           
            for item in params_rol:
                itemRole= Rol.objects.get(id=item)
                # Se construye el objeto para crear los roles
                addRol=Usuario_rol_in_sistema()
                addRol.usuario_asovac=user_asovac
                addRol.rol=itemRole
                addRol.sistema_asovac=arbitraje
                # Para asignar el arbitro al sistema asovac al que pertenece
                if item == "4":
                    arbitro= get_object_or_404(Arbitro,usuario=user_asovac)
                    arbitro.Sistema_asovac.add(arbitraje)
                    arbitro.save()
                addRol.save()
                # form.save()
            data['status']= 200
        else:
            print form.errors
            data['status']= 404
    else:
    
        if(request_user_role > user_role):
            permiso="rol-no-permitido"
        else:
            permiso="rol-permitido"

        data['status']= 200
        data['title']=user.username
        form= AssingRolForm()
        context={
            'user':user,
            'rol_list': rol_list,
            'arbitraje_id':arbitraje_id,
            'tipo':"rol",
            'form':form,
            'permiso':permiso,
            'rol_active':rols,
            'rol_auth':request_user_role,
            'array_rols':array_rols,
            'usuario_asovac':user_asovac,
        }

        data['content']= render_to_string('ajax/BTUsuarios.html',context,request=request)
    
    return JsonResponse(data)