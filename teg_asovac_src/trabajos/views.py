# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decouple import config
from datetime import date
import json, random, string, xlrd, os, sys, xlwt,datetime

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from arbitrajes.models import Arbitro
from autores.forms import AddAuthorToJobForm
from autores.models import Autor, Autores_trabajos,Factura
from main_app.models import Rol,Sistema_asovac,Usuario_asovac,User, Area, Sub_area, Usuario_rol_in_sistema
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status, get_area,exist_email
from main_app.decorators import user_is_arbitraje

from .forms import TrabajoForm, EditTrabajoForm, MessageForm #, AutorObservationsFinalVersionJobForm
from .models import Trabajo, Trabajo_arbitro #, Detalle_version_final
from .tokens import account_activation_token


#Vista donde están la lista de trabajos del autor y dónde se le permite crear, editar o eliminar trabajos
@login_required
def trabajos(request):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
   
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


    usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
    autor = Autor.objects.get(usuario = usuario_asovac)
    sistema_asovac = Sistema_asovac.objects.get(id = arbitraje_id)

    # print items
    if request.method =='POST':
        form = TrabajoForm(request.POST, request.FILES)
        new_subarea = request.POST.get("subarea_select")
        if form.is_valid() and new_subarea != "":
            new_trabajo = form.save()
            subarea_to_assign = Sub_area.objects.get(id = new_subarea)
            codigo = subarea_to_assign.codigo + '-' + str(new_trabajo.id)
            new_trabajo.subareas.add(subarea_to_assign)
            new_trabajo.codigo = codigo
            new_trabajo.save()

            #Código para crear una instancia de Autores_trabajos
            autor_trabajo = Autores_trabajos(autor = autor, trabajo = new_trabajo, es_autor_principal = True, es_ponente = True, sistema_asovac = sistema_asovac, monto_total = sistema_asovac.monto_pagar_trabajo)
            autor_trabajo.save()
            form = TrabajoForm()
            messages.success(request,"Trabajo creado con éxito.")
            return redirect('trabajos:trabajos')
        else:
            if(new_subarea == ""):
                messages.error(request,"Debe elegir un Área - Subárea para el trabajo.")
    else:
        form = TrabajoForm()

    trabajos_list = Autores_trabajos.objects.filter(autor = autor, sistema_asovac = sistema_asovac)
 
    autores_trabajo_list = []

    for autor_trabajo in trabajos_list:
        autores_trabajo_list.append(Autores_trabajos.objects.filter(sistema_asovac = sistema_asovac, trabajo = autor_trabajo.trabajo))

    
    job_data = zip(trabajos_list, autores_trabajo_list)
 
    areas= Area.objects.all().order_by('nombre')
    subarea_list = []
    for area in areas:
        subareas = Sub_area.objects.filter(area = area).order_by('nombre')
        for subarea in subareas:
            subarea_list.append(subarea)
    
    context = {
        "nombre_vista": 'Autores',
        "form": form,
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
        'trabajos': trabajos,
        'areas':areas,
        'subarea_list':subarea_list,
        'job_data': job_data,
        'sistema_asovac': sistema_asovac
    }
    return render(request,"trabajos.html",context)



@login_required
@user_is_arbitraje
def jobs_list(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    # request.session para almacenar el item seleccionado del sidebar
    request.session['sidebar_item'] = "Trabajos"

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    # Seción para obtener área y subarea enviada por sesión y filtrar consulta
    area=request.session['area']
    subarea=request.session['subarea']
    # print "Area y Subarea enviadas por sesion"
    # print area
    # print subarea
    # trabajos=Trabajo.objects.all().filter( Q(subarea1=subarea) | Q(subarea2=subarea) | Q(subarea3=subarea) )
    trabajos=Trabajo.objects.all().filter( )

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    context = {
        'nombre_vista' : 'Trabajos',
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
        'trabajos': trabajos,
    }
    return render(request, 'trabajos_jobs_list.html', context)



@login_required
def jobs_edit(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]



    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items
    context = {
        'nombre_vista' : 'Trabajos',
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
    return render(request, 'trabajos_jobs_edit.html', context)



@login_required
# Vista para editar trabajos
def edit_trabajo(request, trabajo_id):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items
    usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
    autor = Autor.objects.get(usuario = usuario_asovac)
    trabajo = Trabajo.objects.get( id = trabajo_id)
    autor_trabajo = get_object_or_404(Autores_trabajos,  trabajo = trabajo, autor = autor, sistema_asovac = arbitraje_id)

      
    if request.method == 'POST':
        form = EditTrabajoForm(request.POST, request.FILES, instance = autor_trabajo.trabajo)
        if form.is_valid():
            trabajo_edit = form.save()
            trabajo_edit.subareas.clear()
            new_subarea = Sub_area.objects.get(id = request.POST.get("subarea_select"))
            trabajo_edit.subareas.add(new_subarea)
            trabajo_edit.save()
            messages.success(request, 'Sus cambios al trabajo han sido guardados con éxito.')
            return redirect('trabajos:trabajos')
                
    else: 
        form = EditTrabajoForm(instance = autor_trabajo.trabajo)


    areas= Area.objects.all().order_by('nombre')
    subarea_list = []
    for area in areas:
        subareas = Sub_area.objects.filter(area = area).order_by('nombre')
        for subarea in subareas:
            subarea_list.append(subarea)

    subarea_selected = trabajo.subareas.all()[0]
    context = {
        'nombre_vista' : 'Editar Trabajo',
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
        'form':form,
        'trabajo': trabajo,
        'areas': areas,
        'subarea_list':subarea_list,
        'subarea_selected': subarea_selected
    }
    return render(request,"trabajos_edit_trabajo.html",context)



@login_required
#Vista donde aparecen los trabajos evaluados
def trabajos_evaluados(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


    event_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=event_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,event_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, event_id)

    route_conf= get_route_configuracion(estado,rol_id, event_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, event_id)

    # print items

    context = {
        'nombre_vista' : 'Trabajos',
        'main_navbar_options' : main_navbar_options,
        'estado' : estado,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request,"trabajos_trabajos_evaluados.html",context)



@login_required
def detalles_trabajo(request, trabajo_id):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items
    trabajo = Trabajo.objects.get( id = trabajo_id)

    context = {
        'nombre_vista' : 'Editar Trabajo',
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
        'trabajo':trabajo,
        'arbitro_review': False, #Esto es para ocultar los botones para calificar el trabajo 
    }
    return render(request,"trabajos_detalles.html",context)



@login_required
def trabajos_resultados_autor(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print items
    usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
    autor = Autor.objects.get(usuario = usuario_asovac)
    autor_trabajo_list = Autores_trabajos.objects.filter(autor = autor, sistema_asovac = arbitraje_id)

    trabajo_version_final_list = Detalle_version_final.objects.all()

    trabajo_list= []
    for autor_trabajo in autor_trabajo_list:
        for trabajo_version_final in trabajo_version_final_list:
            if autor_trabajo.trabajo == trabajo_version_final.trabajo and trabajo_version_final.estatus_final != "Pendiente":
                trabajo_list.append(trabajo_version_final)
                break

    for trabajo_version_final in trabajo_list:
        print (trabajo_version_final.trabajo.titulo_espanol)


    context = {
        'nombre_vista' : 'Trabajos',
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
        'trabajo_list': trabajo_list,
        'autor_trabajo_list': autor_trabajo_list,
    }
    return render(request,"trabajos_resultados_autor.html",context)



@login_required
def delete_job(request, trabajo_id):
    
    data = dict()
    trabajo = get_object_or_404(Trabajo, id = trabajo_id)
    if request.method == "POST":
        trabajo.delete()
        return redirect('trabajos:trabajos') 
    else:
        context = {
            'trabajo':trabajo,
        }
        data['html_form'] = render_to_string('ajax/job_delete.html',context,request=request)
    return JsonResponse(data)



@login_required
def show_job_observations(request, trabajo_version_final_id):
    data = dict()
    trabajo_version_final = get_object_or_404(Detalle_version_final, id = trabajo_version_final_id)
    context = {
        'trabajo_version_final': trabajo_version_final,
    }
    data['html_form'] = render_to_string('ajax/job_observations.html',context, request=request)
    return JsonResponse(data)



# @login_required
# def autor_add_observations_to_job(request, trabajo_version_final_id):
#     data = dict()
#     trabajo = get_object_or_404(Detalle_version_final, id = trabajo_version_final_id)
#     if request.method == "POST":
#         form = AutorObservationsFinalVersionJobForm(request.POST, instance = trabajo)
#         form.save()
#         messages.success(request,"La observación fue guardada con éxito.")
#         return redirect('trabajos:trabajos_resultados_autor')
#     else:
#         form = AutorObservationsFinalVersionJobForm(instance = trabajo)
#         context = {
#             'trabajo_version_final': trabajo,
#             'form':form,
#         }
#         data['html_form'] = render_to_string('ajax/autor_add_job_observations.html', context, request=request)
#     return JsonResponse(data)



@login_required
#Vista de ajax para añadir autores a un trabajo
def add_author_to_job(request, autor_trabajo_id):
    data = dict()
    arbitraje_id = request.session['arbitraje_id']
    sistema_asovac = get_object_or_404(Sistema_asovac, id = arbitraje_id)
    autor_trabajo = get_object_or_404(Autores_trabajos, id = autor_trabajo_id) 
    if request.method == "POST":
        form = AddAuthorToJobForm(request.POST, autor_trabajo = autor_trabajo)
        if form.is_valid():   
            print("Entro")
            form_data = form.cleaned_data
            autor = get_object_or_404(Autor, correo_electronico = form_data['correo'])
            autor_trabajo_ponente = Autores_trabajos.objects.get(trabajo = autor_trabajo.trabajo, es_ponente = True)
            if form_data['es_ponente']:
                autor_trabajo_ponente.es_ponente = False
                autor_trabajo_ponente.save()
            new_autor_trabajo = Autores_trabajos(autor = autor, trabajo = autor_trabajo.trabajo, sistema_asovac = sistema_asovac ,es_autor_principal = False, es_ponente = form_data['es_ponente'], es_coautor = form_data['es_coautor'], monto_total = autor_trabajo.monto_total)
            new_autor_trabajo.save()
            rol_autor = Rol.objects.get(id=5)

            # Esto es para darle los permisos del rol autor al autor si no está registrado en el sistema
            if not Usuario_rol_in_sistema.objects.filter(rol = rol_autor, sistema_asovac = sistema_asovac, usuario_asovac = autor.usuario).exists():
                new_usuario_rol_in_sistema = Usuario_rol_in_sistema(rol = rol_autor, sistema_asovac = sistema_asovac, usuario_asovac = autor.usuario)
                new_usuario_rol_in_sistema.save()

            messages.success(request,"El autor fue añadido al trabajo con éxito.")
            data['form_is_valid']= True
            data['url'] = reverse('trabajos:trabajos')     

    else: 
        form = AddAuthorToJobForm(autor_trabajo = autor_trabajo) 
    context = {
        'autor_trabajo': autor_trabajo,
        'form':form,
    }
    data['html_form'] = render_to_string('ajax/add_author_to_job.html', context, request=request)
    return JsonResponse(data)




# Ajax/para el uso de ventanas modales
def query_filter(sidebar_item):
    list_elem=""

    if sidebar_item == "Trabajos":
        list_elem= "trabajos"

    if sidebar_item == "Autores":
        list_elem="Autores"
        
    return list_elem
# Se realiza el cambio de subarea y se pasan los parametros necesarios para filtrar contenido



@login_required
def show_areas_modal(request,id):
    # print "ID recibido",id 
    data= dict()
    user= get_object_or_404(User,id=id)
    auth_user=user    
    user= Usuario_asovac.objects.get(usuario_id=id)
    user_role= get_roles(user.id, "is_admin")
    # print "El rol del usuario es: ",user_role
    if(user_role == 1 or user_role == 2):
        subareas= Sub_area.objects.all()
        area= Area.objects.all()
      
    else:
        subareas= user.sub_area.all()
        area= []
        area.append(subareas.first().area)

    # print (area)
    # print (subareas)

    if request.method == 'POST':
        # print "El metodo es post"
        area=request.POST['area_select']
        subarea=request.POST['subarea_select']

        # print area
        # print subarea

        request.session['area']=request.POST['area_select']
        request.session['subarea']=request.POST['subarea_select']

        trabajos=Trabajo.objects.all().filter( Q(subarea1=subarea) | Q(subarea2=subarea) | Q(subarea3=subarea) )

        data['form_is_valid']= True
        data['user_list']= render_to_string('ajax/dinamic_jobs_list.html',{'trabajos':trabajos},request=request)
    else:
        # print "el metodo es get"
        context= {
            'areas': area,
            'subareas':subareas,
            'user': auth_user,
        }
        data['html_form']=render_to_string('ajax/show_areas.html',context,request=request)

    return JsonResponse(data)



#---------------------------------------------------------------------------------#
#                  Carga el contenido de la tabla de arbitros                     #
#---------------------------------------------------------------------------------#
@login_required
def list_trabajos(request):
    
    event_id = request.session['arbitraje_id']
    rol_user=get_roles(request.user.id,event_id)
    user_area=get_area(request.user.id)
    arbitraje_id = request.session['arbitraje_id']
    area= user_area

    # print "El rol del usuario logueado es: ",rol_user
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
        # limit= int(request.POST['limit'])+init
        limit= int(request.POST['limit'])
    
    if request.POST.get('export',False) != False:
        export= request.POST.get('export')
    else:
        export= ""

    if sort == 'pk':
        sort='id'


    if search != "" and export == "":
        print "Consulta Search"
        # data= Usuario_asovac.objects.select_related('arbitro','usuario').filter( Q(usuario__username__contains=search) | Q(usuario__first_name__contains=search) | Q(usuario__last_name__contains=search) | Q(usuario__email__contains=search) ).order_by(order)
        # total= len(data)
        # data=User.objects.all().filter( Q(username__contains=search) | Q(first_name__contains=search) | Q(last_name__contains=search) | Q(email__contains=search) ).order_by(order)#[:limit]
        if rol_user == 1 or rol_user == 2:
            query= "SELECT DISTINCT(trab.id),trab.confirmacion_pago,trab.estatus,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
            query_count=query
            search= search+'%'
            where=' WHERE (trab.estatus like %s or trab.titulo_espanol like %s or trab.forma_presentacion like %s or trab.observaciones like %s or main_a.nombre like %s or main_sarea.nombre like %s or trab.confirmacion_pago like %s ) AND sis_aso.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true '
            query= query+where
        else:
            if rol_user == 3:
                query= "SELECT DISTINCT(trab.id),trab.confirmacion_pago,trab.estatus,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                query_count=query
                search= search+'%'
                where=' WHERE (trab.estatus like %s or trab.titulo_espanol like %s or trab.forma_presentacion like %s or trab.observaciones like %s or main_a.nombre like %s or main_sarea.nombre like %s or trab.confirmacion_pago like %s ) AND sis_aso.id= %s AND main_a.id in ({}) AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true '.format(area)
                query= query+where
        if sort == "nombre":
            order_by="main_a."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
        else:
            order_by="trab."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
        query= query + " ORDER BY " + order_by
        if rol_user == 1 or rol_user ==2 :
            data= User.objects.raw(query,[search,search,search,search,search,search,search,event_id])
            data_count= User.objects.raw(query,[search,search,search,search,search,search,search,event_id])
            # data_count= User.objects.raw(query_count)
        else:
            if rol_user == 3:
                data= User.objects.raw(query,[search,search,search,search,search,search,search,event_id])
                data_count= User.objects.raw(query,[search,search,search,search,search,search,search,event_id])

        total=0

        for item in data_count:
            total=total+1
    else:
        # if request.POST.get('limit', False) == False or request.POST.get('offset', False) == False:
        if export !=  "":
    
            print "Consulta para Exportar Todo"

        else:
            print "Consulta Normal"
            # consulta basica
            # data=User.objects.all().order_by(order)[init:limit].query
            # data=User.objects.all().order_by('pk')[init:limit].query

            # consulta mas completa
            if rol_user == 1 or rol_user == 2:
                query= "SELECT DISTINCT(trab.id),trab.confirmacion_pago,trab.estatus,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                where=' WHERE sis_aso.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true '
                query= query+where
            else:
                if rol_user == 3:
                    query= "SELECT DISTINCT(trab.id),trab.confirmacion_pago,trab.estatus,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                    where=' WHERE sis_aso.id= %s AND main_a.id in ({}) AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true '.format(area)
                    query= query+where
            
            if sort=="nombre":
                order_by="main_a."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
            else:
                order_by="trab."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
            query_count=query
            query= query + " ORDER BY " + order_by
            
            if rol_user == 1 or rol_user ==2 :
                data= User.objects.raw(query,event_id)
                data_count= User.objects.raw(query_count,event_id)
            else:
                if rol_user == 3:
                    data= User.objects.raw(query,[event_id])
                    data_count= User.objects.raw(query_count,[event_id])

            total=0
            for item in data_count:
                total=total+1
  
            # data= Usuario_asovac.objects.select_related('arbitro','usuario').filter( id=27).order_by(order)
            # total= len(data)

    # for item in data:
        # print("%s is %s. and total is %s" % (item.username, item.first_name,item.last_name, item.email))
        # response['query'].append({'id':item.id,'first_name': item.first_name,'last_name':item.last_name,'username': item.username,'email':item.email})
    
    for item in data:
        # estatus= item.estatus 
        autores= Autores_trabajos.objects.filter(trabajo=item.id)
        total_autores= autores.count()
        contador=0
        # print total_autores
        # print "Autores Para el trabajo ", item.id
        list_autores=""
        for aut in autores:
            # print ( "Datos del autor {0} {1}".format(aut.autor.nombres,aut.autor.apellidos))
            if (contador+1) == total_autores: 
                list_autores= list_autores+aut.autor.nombres+" "+aut.autor.apellidos+" "
            else:
                list_autores= list_autores+aut.autor.nombres+" "+aut.autor.apellidos+", "
            contador= contador+1

        # print list_autores
        if item.estatus == "Aceptado":
            estatus= '<span class="label label-success">'+item.estatus +'</span>'
        else:
            if item.estatus == "Rechazado":
                estatus= '<span class="label label-danger">'+item.estatus +'</span>'
            else:
                estatus= '<span class="label label-warning">'+item.estatus +'</span>'
        titulo= item.titulo_espanol
        presentacion= item.forma_presentacion
        
        if item.confirmacion_pago == "Aceptado":
            confirmacion_pago= '<span class="label label-success">'+item.confirmacion_pago +'</span>'
        else:
            if item.confirmacion_pago == "Rechazado":
                confirmacion_pago= '<span class="label label-danger">'+item.confirmacion_pago +'</span>'
            else:
                confirmacion_pago= '<span class="label label-warning">'+item.confirmacion_pago +'</span>'

        if item.observaciones =="": 
            observaciones = "-"
        else:
            observaciones = item.observaciones
        # autor_principal=item.nombres+' '+item.apellidos
        area = item.nombre
        subarea=item.subarea
        response['query'].append({'id':item.id,'estatus': estatus ,'nombre':area,'titulo_espanol':titulo ,'forma_presentacion':presentacion,"confirmacion_pago":confirmacion_pago,"autor_principal":list_autores, 'observaciones':observaciones,'subarea':subarea  })


    response={
        'total': total,
        'query': response,
    }
   
    return JsonResponse(response)

# 
#---------------------------------------------------------------------------------#
#                  Carga el contenido de la tabla de pagos                     #
#---------------------------------------------------------------------------------#
@login_required
def list_pagos(request,id):
    
    # factura= Factura.objects.filter(pagador__autor_trabajo__trabajo=id)
    # comprobante= factura.get().pago.comprobante_pago
    # print factura.query
    # print comprobante    
    # print factura.get().pagador.datos_pagador.nombres
    # print factura.get().pagador.datos_pagador.apellidos
    # print factura.get().pagador.datos_pagador.cedula
    # print factura.get().pagador.apellidos

    response = {}
    response['query'] = []

    sort= request.POST['sort']
    order= request.POST['order']
    
    print "Consulta Normal"
    
    # consulta mas completa
    
    query= "SELECT aut_trab.numero_postulacion AS aut_numero_postulacion, aut_fac.numero_postulacion AS fac_numero_postulacion, aut_fac.id, aut_fac.status, aut_dat_pgd.nombres, aut_dat_pgd.apellidos, aut_dat_pgd.cedula, aut_pag.fecha_pago,aut_dat_pgd.telefono_oficina, aut_dat_pgd.telefono_habitacion_celular, aut_pag.comprobante_pago FROM autores_autores_trabajos AS aut_trab INNER JOIN autores_pagador AS aut_pgd ON aut_pgd.autor_trabajo_id = aut_trab.id INNER JOIN autores_factura AS aut_fac ON aut_fac.pagador_id = aut_pgd.id INNER JOIN autores_pago AS aut_pag ON aut_pag.id= aut_fac.pago_id INNER JOIN autores_datos_pagador AS aut_dat_pgd ON aut_dat_pgd.id= aut_pgd.datos_pagador_id "
    where=' WHERE aut_trab.trabajo_id= %s'
    query= query+where
    
    query_count=query
    query= query + " ORDER BY aut_fac.status" 
    
    data= Factura.objects.raw(query,id)
    data_count= Factura.objects.raw(query_count,id)
    
    total=0
    for item in data_count:
        total=total+1
  
    for item in data:
        # estatus= item.estatus 
        pagador = item.nombres+" "+item.apellidos
        cedula=item.cedula
        comprobante= item.comprobante_pago
        fecha_pago= item.fecha_pago
        telefono_oficina=item.telefono_oficina
        telefono_habitacion_celular=item.telefono_habitacion_celular
        if item.status == "Aceptado":
            status= '<span class="label label-success">'+item.status +'</span>'
        elif item.status == "Rechazado":
            status= '<span class="label label-danger">'+item.status +'</span>'
        else:
            status= '<span class="label label-warning">'+item.status +'</span>'


        if item.aut_numero_postulacion == item.fac_numero_postulacion:
            actual = '<span class="label label-success">Sí</span>'
        else:
            actual = '<span class="label label-danger">No</span>'
        response['query'].append({'id':item.id, 'status':status, "pagador":pagador,"cedula":cedula,"fecha_pago":fecha_pago, "telefono_oficina":telefono_oficina,"telefono_habitacion_celular":telefono_habitacion_celular,"comprobante":comprobante, "actual": actual })
    
    response={
        'total': total,
        'query': response,
    }
   
    return JsonResponse(response)


#---------------------------------------------------------------------------------#
#                                CRUD de Trabajos                                 #
#---------------------------------------------------------------------------------#
# @login_required
def filterArbitro(data,trabajo_id):
    arbitros= []

    for arb in data:
    
        caseNone=arb.trabajo_id == None
        caseExist=str(trabajo_id) == str(arb.trabajo_id)

        if not caseNone and not caseExist:
            # print "No tiene registro asignado a este trabajo"
            isAsig=0
            for item in data:
                if str(trabajo_id) == str(item.trabajo_id):
                    isAsig=1

            for item2 in arbitros:
                if item2['correo_electronico'] == arb.correo_electronico:
                    isAsig=1
            
            if isAsig == 0:
                # print ("Datos del arbitro: {0} {1} {2} {3}".format(arb.nombres,arb.apellidos,arb.correo_electronico,arb.trabajo_id))
                arbitros.append({'id':arb.id,'nombres': arb.nombres,'apellidos':arb.apellidos, 'correo_electronico':arb.correo_electronico, 'trabajo_id':arb.trabajo_id  })

        else:
            if caseNone:
                # print "No existe registro"
                # print ("Datos del arbitro: {0} {1} {2} {3}".format(arb.nombres,arb.apellidos,arb.correo_electronico,arb.trabajo_id))
                arbitros.append({'id':arb.id,'nombres': arb.nombres,'apellidos':arb.apellidos, 'correo_electronico':arb.correo_electronico, 'trabajo_id':arb.trabajo_id  })
            else:
                if caseExist:
                    # print "Ya esta asignado a este trabajo"
                    # print ("Datos del arbitro: {0} {1} {2} {3}".format(arb.nombres,arb.apellidos,arb.correo_electronico,arb.trabajo_id))
                    arbitros.append({'id':arb.id,'nombres': arb.nombres,'apellidos':arb.apellidos, 'correo_electronico':arb.correo_electronico, 'trabajo_id':arb.trabajo_id  })
 
    return arbitros

@login_required
def checkPago(request,id):

    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)
    
    autor_trabajo_principal = Autores_trabajos.objects.get(es_autor_principal = True, trabajo = id)

    pending_review  = Factura.objects.filter(pagador__autor_trabajo__trabajo = id, status__iexact='pendiente', numero_postulacion = autor_trabajo_principal.numero_postulacion).exists()

    rejected_pay = Factura.objects.filter(pagador__autor_trabajo__trabajo = id, status__iexact='rechazado', numero_postulacion = autor_trabajo_principal.numero_postulacion ).exists()

    context = {
        'nombre_vista' : 'Detalle del pago',
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
        'trabajo_id':id,
        'pending_review': pending_review,
        'rejected_pay': rejected_pay
    }
    return render(request,"trabajos_trabajo_pago.html",context)

@login_required
def validatePago(request,id):
    # print request.POST.get("statusPago")
    trabajo = Trabajo.objects.get( id = id)
    pago=request.POST.get("statusPago")
    response= dict()

    if pago == "Aceptado":
        response['status']=200
        response['message']="El estatus del pago ha sido cambiado de manera exitosa"
        trabajo.confirmacion_pago=pago
        trabajo.save()
    else:
        response['status']=200
        response['message']="El estatus del pago ha sido cambiado de manera exitosa"
        trabajo.confirmacion_pago=pago
        trabajo.save()

    return JsonResponse(response)

@login_required
def review_pay(request, factura_id):
    data = dict()
    event_id = request.session['arbitraje_id']
    factura = get_object_or_404(Factura, id = factura_id)
    autor_trabajo = get_object_or_404(Autores_trabajos, sistema_asovac = event_id, trabajo = factura.pagador.autor_trabajo.trabajo, es_autor_principal = True)

    if request.method =='POST':
        pago = request.POST.get("statusPago")
        form = MessageForm(request.POST)
        if pago:
            if pago.lower() == 'aceptado':     
                factura.status = pago
                factura.save()
                messages.success(request,"Se ha cambiado el estatus a del pago a 'aceptado' con éxito.")
                return redirect('trabajos:checkPago', id = factura.pagador.autor_trabajo.trabajo.id)
            elif pago.lower() == 'rechazado':
                form = MessageForm()
                context = {
                    'factura': factura,
                    'form': form
                }
                data['html_form'] = render_to_string('ajax/decline_pay_reasons.html', context, request = request)
                return JsonResponse(data)
        elif form.is_valid():
            factura.observacion_coordinador = form.cleaned_data['motivo_rechazo']
            factura.status = 'Rechazado'
            factura.save()
            messages.success(request, "Se ha cambiado el estados del pago a 'rechazado' con éxito." )
            return redirect('trabajos:checkPago', id = factura.pagador.autor_trabajo.trabajo.id)
    context ={
		'factura': factura,
        'review_mode': True
	}
    data['html_form'] = render_to_string('ajax/postular_trabajo_pay_details.html', context, request=request)
    return JsonResponse(data)

@login_required
def selectArbitro(request,id):
    # print "Trabajo id: ",id

    event_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=event_id)
    rol_user=get_roles(request.user.id,event_id)
    user_area=get_area(request.user.id)
    subAreaTrabajo= Trabajo.objects.get(id=id).subareas.get().id
    
    if rol_user == 1 or rol_user == 2:
        query= "SELECT DISTINCT (arb.nombres),arb.apellidos,arb.id,arb_trab.trabajo_id, arb.correo_electronico FROM arbitrajes_arbitro AS arb INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS sis_aso ON sis_aso.arbitro_id = arb.id INNER JOIN main_app_usuario_asovac AS usu_aso ON usu_aso.id = arb.usuario_id INNER JOIN main_app_usuario_asovac_sub_area AS usu_sub_a ON usu_sub_a.usuario_asovac_id = usu_aso.id INNER JOIN main_app_sub_area AS sub_a ON sub_a.id = usu_sub_a.sub_area_id LEFT JOIN trabajos_trabajo_subareas AS trab_sub_a ON trab_sub_a.sub_area_id = sub_a.id LEFT JOIN trabajos_trabajo_arbitro AS arb_trab on arb.id = arb_trab.arbitro_id"
        where=' WHERE sis_aso.sistema_asovac_id = %s and usu_sub_a.sub_area_id= {}'.format(subAreaTrabajo)      
        query= query+where
    else:
        if rol_user == 3:
            query= "SELECT DISTINCT (arb.nombres),arb.apellidos,arb.id,arb_trab.trabajo_id, arb.correo_electronico FROM arbitrajes_arbitro AS arb INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS sis_aso ON sis_aso.arbitro_id = arb.id INNER JOIN main_app_usuario_asovac AS usu_aso ON usu_aso.id = arb.usuario_id INNER JOIN main_app_usuario_asovac_sub_area AS usu_sub_a ON usu_sub_a.usuario_asovac_id = usu_aso.id INNER JOIN main_app_sub_area AS sub_a ON sub_a.id = usu_sub_a.sub_area_id LEFT JOIN trabajos_trabajo_subareas AS trab_sub_a ON trab_sub_a.sub_area_id = sub_a.id LEFT JOIN trabajos_trabajo_arbitro AS arb_trab on arb.id = arb_trab.arbitro_id"
            where=' WHERE sis_aso.sistema_asovac_id = %s and usu_sub_a.sub_area_id= {}'.format(subAreaTrabajo)  
            query= query+where

    
    order_by="arb.nombres " 
    query_count=query
    query= query + " ORDER BY " + order_by
    
    if rol_user == 1 or rol_user ==2 :
        data= Arbitro.objects.raw(query,[event_id])
        data_count= Arbitro.objects.raw(query_count,[event_id])
    else:
        if rol_user == 3:
            data= Arbitro.objects.raw(query,[event_id])
            data_count= Arbitro.objects.raw(query_count,[event_id])

    total=0
    datafilter= filterArbitro(data,id)

    for item in data_count:
        total=total+1

    response=dict()
    arbitros= []



    if request.method == 'POST':
        # print "El metodo es post"
        form=request.POST
        # print form.values()
        # print "id de los arbitros ",form['id']
        # print "id del trabajos ",form['trabajo']
        # trabajo= Trabajo.objects.get(id=id)

        if form['id'] == '':
            # print "el formulario viene vacio"
            listArbTrab= Trabajo_arbitro.objects.filter(trabajo_id=id).delete()
        else:
            # print "el formulario no viene vacio"
            listArbId =""
            list_arbitros= form['id'].split(",")
            # Para dar formato al arary de id para el query
            totalArbitros=len(list_arbitros)
            cont=1
            # print totalArbitros
            for arb_id in list_arbitros:
                if totalArbitros > 1:
                    if cont < totalArbitros:
                        listArbId= listArbId+str(arb_id)+","
                    else:
                        listArbId= listArbId+str(arb_id)
                else:
                    listArbId= listArbId+str(arb_id)
                cont= cont+1
 
            # consulta para eliminar registros no seleccionados
            query= "DELETE FROM trabajos_trabajo_arbitro "
            where="WHERE trabajos_trabajo_arbitro.trabajo_id={} and trabajos_trabajo_arbitro.arbitro_id not in ({})".format(id,listArbId)
            query= query+where
            cursor = connection.cursor()
            cursor.execute(query)

            # print Trabajo_arbitro.objects.extra(where=["trabajos_trabajo_arbitro.trabajo_id= %s and trabajos_trabajo_arbitro.arbitro_id not in(%s)"],params=[id,listArbId]).query
            # listArbTrab=Trabajo_arbitro.objects.extra(where=["trabajos_trabajo_arbitro.trabajo_id= %s and trabajos_trabajo_arbitro.arbitro_id not in(%s)"],params=[id,listArbId]).delete()
            # return HttpResponse(str("Exit"))
            # listArbTrab= Trabajo_arbitro.objects.filter(trabajo_id=id).delete()
            for arb in list_arbitros:
                print("holis")
                # print listArbTrab
                trabajo= Trabajo.objects.get(id=id)
                arbitro= Arbitro.objects.get(id=arb)
                # Para verificar si el registro existe
                if Trabajo_arbitro.objects.filter(arbitro=arb, trabajo = trabajo).exists() == False:
                    # Se crea la instancia de arbitros y trabajos 
                    arbitroTrabajo= Trabajo_arbitro()
                    arbitroTrabajo.fin_arbitraje= False
                    arbitroTrabajo.invitacion= False
                    arbitroTrabajo.trabajo=trabajo
                    arbitroTrabajo.arbitro=arbitro
                    arbitroTrabajo.save()

                    # Se crean parametros para el correo 
                    url_site = get_current_site(request)
                    arb_id=urlsafe_base64_encode(force_bytes(arbitro.pk))
                    token= account_activation_token.make_token(arbitro)
                    inv_id=urlsafe_base64_encode(force_bytes(arbitroTrabajo.pk))

                    # print ("Datos Correo: {0} {1} {2} {3} {4} {5}".format(url_site,arbitro.apellidos,arbitro.nombres,arbitro.correo_electronico,arb_id,token))

                    # Correo de asignacion a trabajos con token de confirmacion
                    context = {
                        'invitacion':inv_id,
                        'url_site':url_site,
                        'arbitro':arbitro,
                        'arb_id':arb_id,
                        'token':token,
                        'trabajo':trabajo.titulo_espanol,
                        'arbitraje':arbitraje,
                    }
                    msg_plain = render_to_string('../templates/email_templates/create_invitation.txt', context)
                    msg_html = render_to_string('../templates/email_templates/create_invitation.html', context)

                    send_mail(
                        'Asignación de trabajo para revisión',              #titulo
                        msg_plain,                                          #mensaje txt
                        config('EMAIL_HOST_USER'),                          #email de envio
                        [arbitro.correo_electronico],                       #destinatario
                        html_message=msg_html,                              #mensaje en html
                        )

        response['status']= 200
            # response['status']= 404
            
    else:
       
        response['status']= 200
        context={
            'tipo':"select",
            'arbitros':datafilter,
            'trabajo_id':int(id),
        }
        response['content']= render_to_string('ajax/BTTrabajos.html',context,request=request)
    return JsonResponse(response)



@login_required
def viewTrabajo(request, id):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    arbitraje_id = request.session['arbitraje_id']
    arbitraje = Sistema_asovac.objects.get(pk=arbitraje_id)
    estado = arbitraje.estado_arbitraje
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    # print request.user
    # usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
    # autor = Autor.objects.get(usuario = usuario_asovac)
    trabajo = Trabajo.objects.get( id = id)
    area=trabajo.subareas.all()[0].area.nombre
    subarea=trabajo.subareas.all()[0].nombre
    # autor_trabajo = get_object_or_404(Autores_trabajos,  trabajo = trabajo, sistema_asovac = arbitraje_id)
    # autor_trabajo = get_object_or_404(Autores_trabajos,  trabajo = trabajo, autor = autor, sistema_asovac = arbitraje_id)

    context = {
        'nombre_vista' : 'Detalle Trabajo',
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
        # 'autor_trabajo':autor_trabajo,
        'area':area,
        'subarea':subarea,
        'trabajo':trabajo,
    }
    return render(request,"trabajos_trabajo_info.html",context)



@login_required
def invitacion(request, uidb64, token):
    try:
        invitacion_id = force_text(urlsafe_base64_decode(uidb64))
        invitacion = Trabajo_arbitro.objects.get(pk=invitacion_id)
        arbitro= Arbitro.objects.get(id=invitacion.arbitro.id)
    except(TypeError, ValueError, OverflowError, Trabajo_arbitro.DoesNotExist):
        invitacion = None

    if invitacion is not None and account_activation_token.check_token(arbitro, token):
        invitacion.invitacion=True
        invitacion.save()
        status=200
        msj= "Su invitación ha sido confirmada de manera exitosa"
    else:
        status=404
        msj= "Ha ocurrido un problema y no se ha podido confirman su invitación"

    context={
            'msj':msj,
            'status':status,
        }
    # print "Invitacion: {0} {1}".format (invitacion.id,invitacion.arbitro.id)
    return render(request,"trabajos_invitation.html",context)



@login_required
def viewEstatus(request,id):
    # print "Trabajo id: ",id

    response= dict()
    
    # Consulta
    query= "SELECT trab_arb.*, arb.* FROM trabajos_trabajo_arbitro AS trab_arb INNER JOIN arbitrajes_arbitro AS arb ON trab_arb.arbitro_id = arb.id"
    where=' WHERE trabajo_id= %s '
    query= query+where

    
    order_by="arb.nombres " 
    query_count=query
    query= query + " ORDER BY " + order_by
    
    arbitros= Arbitro.objects.raw(query,[str(id)])

    if request.method == 'POST':
      
        response['status']= 200
        # response['status']= 404
            
    else:
       
        response['status']= 200
        context={
            'tipo':"status",
            'arbitros':arbitros,
        }
        response['content']= render_to_string('ajax/BTTrabajos.html',context,request=request)
    return JsonResponse(response)



#---------------------------------------------------------------------------------#
#                               Exportar Arbitro                                  #
#---------------------------------------------------------------------------------#
@login_required
def generate_report(request,tipo):
    print "Excel para trabajos"
    event_id = request.session['arbitraje_id']
    rol_user=get_roles(request.user.id,event_id)
    user_area=get_area(request.user.id)
    arbitraje_id = request.session['arbitraje_id']
    area= user_area
    # Fecha
    date=datetime.datetime.now()
    date=date.year
    
    # Para exportar información de los trabajos
    if tipo == '1':
        if rol_user == 1 or rol_user == 2:
                query= "SELECT DISTINCT(trab.id),trab.confirmacion_pago,trab.estatus,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                where=' WHERE sis_aso.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true '
                query= query+where
        else:
            if rol_user == 3:
                query= "SELECT DISTINCT(trab.id),trab.confirmacion_pago,trab.estatus,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                where=' WHERE sis_aso.id= %s AND main_a.id in ({}) AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true '.format(area)
                query= query+where
        
        
        order_by=" ORDER BY trab.id asc"
        query_count=query
        query= query + order_by
        
        if rol_user == 1 or rol_user ==2 :
            data= User.objects.raw(query,event_id)
            data_count= User.objects.raw(query_count,event_id)
        else:
            if rol_user == 3:
                data= User.objects.raw(query,[event_id])
                data_count= User.objects.raw(query_count,[event_id])

        total=0
        for item in data_count:
            total=total+1

        # Para definir propiedades del documento de excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=convencion_asovac_{}_lista_de_trabajos.xls'.format(date)
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet("Usuarios")
        # Para agregar los titulos de cada columna
        row_num = 0
        columns = ['Estatus', 'Área','Subárea', 'Título','Presentación','Pago','Observaciones']
        for col_num in range(len(columns)):
            worksheet.write(row_num, col_num, columns[col_num])     
        
        for item in data:
            row_num += 1
            row = [item.estatus ,item.nombre,item.subarea ,item.titulo_espanol ,item.forma_presentacion,item.confirmacion_pago,item.observaciones]
            for col_num in range(len(row)):
                worksheet.write(row_num, col_num, row[col_num])
        
        workbook.save(response)

    else:
        if tipo== '2':
            print "Estatus del arbitraje"
            if rol_user == 1 or rol_user == 2:
                query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                where=" WHERE sis_aso.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true AND trab.confirmacion_pago='Aceptado' "
                query= query+where
            else:
                if rol_user == 3:
                    query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                    where=" WHERE sis_aso.id= %s AND main_a.id in ({}) AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true AND trab.confirmacion_pago='Aceptado' ".format(area)
                    query= query+where

            order_by=" ORDER BY trab.id asc"
            query_count=query
            query= query + order_by

            if rol_user == 1 or rol_user ==2 :
                data= User.objects.raw(query,event_id)
                data_count= User.objects.raw(query_count,event_id)
            else:
                if rol_user == 3:
                    data= User.objects.raw(query,[event_id])
                    data_count= User.objects.raw(query_count,[event_id])
           
            total=0
            for item in data_count:
                total=total+1

            # Para definir propiedades del documento de excel
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=convencion_asovac_{}_estatus_de_trabajos.xls'.format(date)
            workbook = xlwt.Workbook()
            worksheet = workbook.add_sheet("Usuarios")
            # Para agregar los titulos de cada columna
            row_num = 0
            columns = ['Estatus', 'Área','Subárea', 'Título','Presentación','Version','Observaciones']
            for col_num in range(len(columns)):
                worksheet.write(row_num, col_num, columns[col_num])     
            
            for item in data:
                if item.requiere_arbitraje == False and item.estatus == "Aceptado":
                    revision="Final"
                else:
                    if item.estatus == "Pendiente":
                        revision="Sin revisar"
                    else:
                        if item.estatus == "Rechazado":
                            revision="Final"
                        else:
                            revision="Con correcciones"
                row_num += 1
                row = [item.estatus ,item.nombre,item.subarea ,item.titulo_espanol ,item.forma_presentacion,revision,item.observaciones]
                for col_num in range(len(row)):
                    worksheet.write(row_num, col_num, row[col_num])
            
            workbook.save(response)
        else:
            # print "tipo 3"
            if tipo== '3':
                if rol_user == 1 or rol_user == 2:
                    query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,aut.nombres,aut.apellidos,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                    where=" WHERE sis_aso.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true AND trab.estatus='Aceptado' AND trab.confirmacion_pago='Aceptado' "
                    query= query+where
                else:
                    if rol_user == 3:
                        query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,aut.nombres,aut.apellidos,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                        where=" WHERE sis_aso.id= %s AND main_a.id in ({}) AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true AND trab.estatus='Aceptado' AND trab.confirmacion_pago='Aceptado' ".format(area)
                        query= query+where

                order_by=" ORDER BY trab.id asc"
                query_count=query
                query= query + order_by
                
                if rol_user == 1 or rol_user ==2 :
                    data= User.objects.raw(query,event_id)
                    data_count= User.objects.raw(query_count,event_id)
                else:
                    if rol_user == 3:
                        data= User.objects.raw(query,[event_id])
                        data_count= User.objects.raw(query_count,[event_id])

                total=0
                for item in data_count:
                    total=total+1

                # Para definir propiedades del documento de excel
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename=convencion_asovac_{}_trabajos_aceptados.xls'.format(date)
                workbook = xlwt.Workbook()
                worksheet = workbook.add_sheet("Usuarios")
                # Para agregar los titulos de cada columna
                row_num = 0
                columns = ['Estatus', 'Área','Subárea', 'Título','Presentación','Version','Observaciones']
                for col_num in range(len(columns)):
                    worksheet.write(row_num, col_num, columns[col_num])     
                
                for item in data:
                    if item.requiere_arbitraje == False and item.estatus == "Aceptado":
                        revision="Final"
                    else:
                        if item.estatus == "Pendiente":
                            revision="Sin revisar"
                        else:
                            if item.estatus == "Rechazado":
                                revision="Final"
                            else:
                                revision="Con correcciones"
                    row_num += 1
                    row = [item.estatus ,item.nombre,item.subarea ,item.titulo_espanol ,item.forma_presentacion,revision,item.observaciones]
                    for col_num in range(len(row)):
                        worksheet.write(row_num, col_num, row[col_num])
            
                workbook.save(response)

    return response



@login_required
def add_new_version_to_job(request, last_version_trabajo_id):
    data = dict()
    trabajo = get_object_or_404(Trabajo, id = last_version_trabajo_id)
    if request.method == "POST":
        form = TrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            #Se almacena la nueva versión del trabajo
            job_new_version = form.save(commit = False)
            job_new_version.confirmacion_pago = "Aceptado"
            job_new_version.save()
            subarea_to_assign = trabajo.subareas.first()
            job_new_version.codigo = trabajo.codigo
            job_new_version.subareas.add(subarea_to_assign)
            
            #Se coloca el padre a la nueva versión
            if(trabajo.padre == 0):    
                job_new_version.padre = trabajo.id
            else:
                job_new_version.padre = trabajo.padre
            job_new_version.save()
            
            #Se conecta la nueva versión del trabajo con su "padre"
            trabajo.trabajo_version = job_new_version
            trabajo.save()

            #Se actualiza la tabla autores_trabajos con la última versión del trabajo
            autores_trabajo_list = Autores_trabajos.objects.filter(trabajo = trabajo)
            for autores_trabajo in autores_trabajo_list:
                autores_trabajo.trabajo = job_new_version
                autores_trabajo.save()

            #Se generan automáticamente las invitaciones a los arbitros que llevaron a cabo su arbitraje en la versión anterior.
            trabajo_arbitros = Trabajo_arbitro.objects.filter(trabajo = trabajo, invitacion = True)

            for trabajo_arbitro in trabajo_arbitros:
                new_invitation = Trabajo_arbitro(arbitro = trabajo_arbitro.arbitro, trabajo = job_new_version, invitacion = True)
                new_invitation.save()
                
            messages.success(request,"Se ha creado la nueva versión del trabajo con éxito.")
            data['form_is_valid'] = True
            data['url'] = reverse('trabajos:trabajos')
    else:
        form = TrabajoForm()
    
    context = {
        'last_version_trabajo': trabajo,
        'form':form,
    }
    data['html_form'] = render_to_string('ajax/job_create_new_version_modal.html', context, request=request)
    return JsonResponse(data)



@login_required
def view_referee_observation(request, trabajo_id):
    data = dict()
    trabajo = get_object_or_404(Trabajo, id = trabajo_id) 
    
    context = {
        'trabajo': trabajo,
    }
    data['html_form'] = render_to_string('ajax/referee_job_observations.html', context, request=request)
    return JsonResponse(data)


@login_required
def request_new_pay(request, trabajo_id):
    data = dict()
    autores_trabajo = Autores_trabajos.objects.filter(trabajo__id = trabajo_id)
    if request.method == "POST":
        emails_list = []
        form = MessageForm(request.POST)
        autor_principal = Autores_trabajos.objects.get(trabajo__id = trabajo_id, es_autor_principal = True)
        if form.is_valid() and not Factura.objects.filter(pagador__autor_trabajo__trabajo = autor_principal.trabajo.id, status__iexact = "pendiente"):
            monto_deuda = 0
            facturas = Factura.objects.filter(pagador__autor_trabajo__trabajo = autor_principal.trabajo.id)
            for factura in facturas:
                if factura.status.lower() == "rechazado" and factura.pagador.autor_trabajo.numero_postulacion == factura.numero_postulacion:
                    monto_deuda += factura.monto_total
                elif factura.status.lower() =='aceptado':
                    factura.numero_postulacion += 1
                    factura.save()

            razones_rechazo = form.cleaned_data['motivo_rechazo']
            sistema = Sistema_asovac.objects.get(id = request.session['arbitraje_id'])
            for autor_trabajo in autores_trabajo:   
                emails_list.append(autor_trabajo.autor.correo_electronico)
                autor_trabajo.pagado = False
                autor_trabajo.esperando_modificacion_pago =  True
                autor_trabajo.monto_total += monto_deuda
                autor_trabajo.numero_postulacion += 1
                autor_trabajo.save()

            context = {
            'sistema': sistema.nombre,
            'trabajo': autores_trabajo.first().trabajo,
            'razones_rechazo': razones_rechazo
            }
            msg_plain = render_to_string('../templates/email_templates/request_new_pay.txt', context)
            msg_html = render_to_string('../templates/email_templates/request_new_pay.html', context)

            value = send_mail(
                'Error en pagos de postular trabajo',           #titulo
                msg_plain,                                      #mensaje txt
                config('EMAIL_HOST_USER'),                      #email de envio
                emails_list,                                    #destinatario
                html_message=msg_html,                          #mensaje en html
            )
            if value == 1:
                messages.success(request, "Se han solicitado los nuevos pagos con éxito.")
            else:
                message = "Hubo un error en el envío de correos, por favor pongase en contacto con el autor principal del trabajo, este es su correo electrónico: " + autor_principal.autor.correo_electronico 
                messages.success(request, message)

            return redirect('trabajos:jobs_list')
        else:
            messages.error(request, "No puede enviar solicitud de pago, todavía tiene pagos pendientes por revisar")
            return redirect('trabajos:checkPago', id = autor_principal.trabajo.id)
    else:
        form = MessageForm()
    
    context = {
        'form':form,
        'trabajo': autores_trabajo.first().trabajo
    }
    data['html_form'] = render_to_string('ajax/message_form_modal.html', context, request=request)
    return JsonResponse(data)