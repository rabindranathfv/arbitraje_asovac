# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, date
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin, messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.db import connection

import random, string,xlrd,os,sys,xlwt
from autores.models import Autores_trabajos
from main_app.models import Rol,Sistema_asovac,Usuario_asovac, Sub_area,Area
from trabajos.models import Trabajo_arbitro, Trabajo
from .models import Arbitro
from trabajos.models import Trabajo, Detalle_version_final,Trabajo_arbitro
from sesiones.models import Sesion

from autores.models import Autor, Autores_trabajos
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status, get_area,exist_email
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .forms import ArbitroForm, RefereeCommentForm

# Create your views here.
@login_required
def arbitrajes_pag(request):
    context = {
        "nombre_vista": 'Arbitrajes'
    }
    return render(request,"test_views.html",context)



@login_required
def estatus_trabajos(request):

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
        'nombre_vista' : 'Arbitrajes',
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
    return render(request, 'arbitrajes_trabajos_list.html', context)



@login_required
def jobs_for_review(request):
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

    user = request.user
    usuario_asovac = Usuario_asovac.objects.get(usuario = user)
    arbitro = Arbitro.objects.get(usuario = usuario_asovac)

    trabajos_arbitro_list = Trabajo_arbitro.objects.filter(arbitro = arbitro, fin_arbitraje = False, invitacion = True)
    autores_trabajo_list = []
    for trabajo_arbitro in trabajos_arbitro_list:
        autores_trabajo_list.append(Autores_trabajos.objects.filter(trabajo = trabajo_arbitro.trabajo))

    job_data = zip(trabajos_arbitro_list, autores_trabajo_list)
    context = {
        'nombre_vista' : 'Listado de Trabajos por arbitrar',
        'estado' : estado,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'arbitraje_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'job_data': job_data
    }
    return render(request, 'arbitrajes_jobs_for_review.html', context)



@login_required
def detalles_resumen(request, id_trabajo):
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

    trabajo = Trabajo.objects.get(id = id_trabajo)

    context = {
        'nombre_vista' : 'Detalles Resumen',
        'estado' : estado,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'arbitraje_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
        'trabajo': trabajo,
        'arbitro_review': True, #Booleano para mostrar botones para calificar trabajo
    }
    return render(request, 'trabajos_detalles.html', context)



@login_required
def referee_list(request):

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

    context = {
        'nombre_vista' : 'Listado de Arbitros',
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
    return render(request, 'arbitrajes_referee_list.html', context)



@login_required
def referee_edit(request):

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
        'nombre_vista' : 'Arbitros',
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
    return render(request, 'main_app_referee_edit.html', context)



@login_required
def areas_subareas(request):

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
    return render(request, 'arbitrations_areas_subareas.html', context)



@login_required
def asignacion_de_sesion(request):

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
        'nombre_vista' : 'Asignación de Sesiones',
        'estado' : estado,
        'rol_id' : rol_id,
        'event_id' : event_id,
        'arbitraje_id' : event_id,
        'item_active' : item_active,
        'items':items,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'arbitrajes_asignacion_de_sesion.html', context)



#---------------------------------------------------------------------------------#
#                  Carga el contenido de la tabla de arbitros                     #
#---------------------------------------------------------------------------------#
@login_required
def list_arbitros(request):

    event_id = request.session['arbitraje_id']
    rol_user=get_roles(request.user.id,event_id)
    user_area=get_area(request.user.id)

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
        if rol_user == 1 or rol_user == 2:
            query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS asa ON asa.arbitro_id = arb.id"
            query_count=query
            search= search+'%'
            where=' WHERE arb.nombres like %s or arb.apellidos like %s or arb.genero like %s or arb.correo_electronico like %s or arb.titulo like %s or arb.cedula_pasaporte like %s or arb.linea_investigacion like %s '
            # where=' WHERE au.first_name LIKE %s'
            query= query+where
        else:
            if rol_user == 3:
                query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS asa ON asa.arbitro_id = arb.id"
                search= search+'%'
                where=' WHERE (arb.nombres like %s or arb.apellidos like %s or arb.genero like %s or arb.correo_electronico like %s or arb.titulo like %s or arb.cedula_pasaporte like %s or arb.linea_investigacion like %s) and a.id= %s '
                # where=' WHERE au.first_name LIKE %s'
                query= query+where
                query_count=query

        order_by="au."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init)
        query= query + " ORDER BY " + order_by
        if rol_user == 1 or rol_user ==2 :
            data= User.objects.raw(query,[search,search,search,search,search,search,search])
            data_count= User.objects.raw(query,[search,search,search,search,search,search,search])
            # data_count= User.objects.raw(query_count)
        else:
            if rol_user == 3:
                area= str(user_area.id)
                data= User.objects.raw(query,[search,search,search,search,search,search,search,area])
                data_count= User.objects.raw(query_count,[search,search,search,search,search,search,search,area])

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
            if rol_user == 1 or rol_user == 2:
                query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS asa ON asa.arbitro_id = arb.id"
            else:
                if rol_user == 3:
                    query= "SELECT DISTINCT arb.id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS asa ON asa.arbitro_id = arb.id"
                    where=' WHERE a.id=  %s '
                    query= query+where

            order_by="au."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init)
            query_count=query
            query= query + " ORDER BY " + order_by

            if rol_user == 1 or rol_user ==2 :
                data= Arbitro.objects.raw(query)
                data_count= Arbitro.objects.raw(query_count)
            else:
                if rol_user == 3:
                    area= str(user_area.id)
                    data= Arbitro.objects.raw(query,area)
                    data_count= Arbitro.objects.raw(query_count,area)

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
        genero= item.genero
        response['query'].append({'id':item.id,'first_name': first_name ,'last_name':last_name ,'genero':genero ,'email':email  , 'nombre':area  , 'linea_investigacion':linea_investigacion , 'cedula_pasaporte':cedula_pasaporte,'titulo':titulo })


    response={
        'total': total,
        'query': response,
    }

    return JsonResponse(response)

#---------------------------------------------------------------------------------#
#            Carga el contenido de la tabla de áreas para árbitros                #
#---------------------------------------------------------------------------------#
@login_required
def list_areas_arbitros(request,id):
    
    event_id = request.session['arbitraje_id']
    # print "El rol del usuario logueado es: ",rol_user
    response = {}
    response['query'] = []

    sort= request.POST['sort']
    order= request.POST['order']
    # search= request.POST['search']

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


    print "Consulta Normal"
    arbitraje_id = request.session['arbitraje_id']

    # consulta mas completa
    query= "SELECT DISTINCT ar.id,ar.nombre, ar.codigo, ar.descripcion FROM arbitrajes_arbitro AS arb INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS sis_aso on sis_aso.arbitro_id = arb.id INNER JOIN main_app_usuario_asovac AS usu_aso on usu_aso.id = arb.usuario_id INNER JOIN main_app_usuario_asovac_sub_area AS usu_sub_a on usu_sub_a.usuario_asovac_id = usu_aso.id INNER JOIN main_app_sub_area AS sub_a on sub_a.id = usu_sub_a.sub_area_id INNER JOIN main_app_area AS ar on ar.id= sub_a.area_id"
    where=' WHERE sis_aso.sistema_asovac_id =%s AND usu_aso.id=%s '
    # where=' WHERE sis_aso.sistema_asovac_id =1 and arb.id=8 '
    query= query+where
    query_count=query

    if sort != "pk":
        order_by="ar."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init)
        query= query + " ORDER BY " + order_by

    data= Arbitro.objects.raw(query,[event_id,id])
    data_count= Arbitro.objects.raw(query_count,[event_id,id])

    total=0
    for item in data_count:
        total=total+1

    for item in data:
        nombre= item.nombre
        codigo= item.codigo
        descripcion= item.descripcion
        response['query'].append({'id':item.id,'nombre': nombre ,'codigo':codigo ,'descripcion':descripcion  })


    response={
        'total': total,
        'query': response,
    }

    return JsonResponse(response)

#---------------------------------------------------------------------------------#
#          Carga el contenido de la tabla de subáreas para árbitros               #
#---------------------------------------------------------------------------------#
@login_required
def list_subareas_arbitros(request,id):

    event_id = request.session['arbitraje_id']
    # print "El rol del usuario logueado es: ",rol_user
    response = {}
    response['query'] = []

    sort= request.POST['sort']
    order= request.POST['order']
    # search= request.POST['search']

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

    print "Consulta Normal"
    arbitraje_id = request.session['arbitraje_id']

    # consulta mas completa
    query= "SELECT usu_sub_a.id, sub_a.nombre,sub_a.codigo,sub_a.descripcion FROM arbitrajes_arbitro AS arb INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS sis_aso on sis_aso.arbitro_id = arb.id INNER JOIN main_app_usuario_asovac AS usu_aso on usu_aso.id = arb.usuario_id INNER JOIN main_app_usuario_asovac_sub_area AS usu_sub_a on usu_sub_a.usuario_asovac_id = usu_aso.id INNER JOIN main_app_sub_area AS sub_a on sub_a.id = usu_sub_a.sub_area_id INNER JOIN main_app_area AS ar on ar.id= sub_a.area_id"
    where=' WHERE sis_aso.sistema_asovac_id =%s AND usu_aso.id=%s '
    # where=' WHERE sis_aso.sistema_asovac_id =1 and arb.id=8 '
    query= query+where
    query_count=query

    if sort != "pk":
        order_by="ar."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init)
        query= query + " ORDER BY " + order_by

    data= Arbitro.objects.raw(query,[event_id,id])
    data_count= Arbitro.objects.raw(query_count,[event_id,id])

    total=0
    for item in data_count:
        total=total+1

    for item in data:
        nombre= item.nombre
        codigo= item.codigo
        descripcion= item.descripcion
       
        response['query'].append({'id':item.id,'nombre': nombre ,'codigo':codigo ,'descripcion':descripcion  })


    response={
        'total': total,
        'query': response,
    }

    return JsonResponse(response)


#---------------------------------------------------------------------------------#
#                                 Crud Arbitros                                   #
#---------------------------------------------------------------------------------#
@login_required
def viewArbitro(request,id):

    data= dict()
    user=User.objects.get(id=id)
    user_asovac= Usuario_asovac.objects.get(usuario=id)
    arbitro= Arbitro.objects.get(usuario=user_asovac)

    data['status']= 200
    context={
        'arbitro':arbitro,
        'tipo':"show"
    }
    data['content']= render_to_string('ajax/BTArbitros.html',context,request=request)
    return JsonResponse(data)



@login_required
def editArbitro(request,id):
    print "Edit Arbitro"
    data= dict()
    user=User.objects.get(id=id)
    user_asovac= Usuario_asovac.objects.get(usuario=id)
    arbitro= Arbitro.objects.get(usuario=user_asovac)

    if request.method == 'POST':

        form= ArbitroForm(request.POST,instance=arbitro)
        if form.is_valid():

            if exist_email(request.POST.get("correo_electronico")):
                # print "El correo existe"
                user_email=User.objects.get(email=request.POST.get("correo_electronico"))
                if user.id == user_email.id:
                    # print "Cuando el correo a actualizar es para el mismo usuario"
                    user.first_name=request.POST.get("nombres")
                    user.last_name=request.POST.get("apellidos")
                    user.email=request.POST.get("correo_electronico")
                    user.save()
                    form.save()
                    data['status']= 200
                else:
                    # print "El correo ya esta siendo usado por otra persona"
                    data['status']= 404
            else:
                # Cuando el correo no se repite
                user.first_name=request.POST.get("nombres")
                user.last_name=request.POST.get("apellidos")
                user.email=request.POST.get("correo_electronico")
                user.save()
                form.save()
                data['status']= 200
        else:
            data['status']= 404
    else:

        data['status']= 200
        form= ArbitroForm(instance=arbitro)
        context={
            'tipo':"edit",
            'arbitro_id':id,
            'form':form,
        }
        data['content']= render_to_string('ajax/BTArbitros.html',context,request=request)
    return JsonResponse(data)



@login_required
def removeArbitro(request,id):

    print "eliminar arbitro"
    data= dict()

    user=User.objects.get(id=id)
    user_asovac= Usuario_asovac.objects.get(usuario=id)
    arbitro= Arbitro.objects.get(usuario=user_asovac)
    sistema_asovac= request.session['arbitraje_id']

    if request.method == 'POST':
        # print "post delete form"
        arbitro=Arbitro.objects.get(usuario=user_asovac,Sistema_asovac=sistema_asovac)
        arbitro.Sistema_asovac.remove(sistema_asovac)

        data['status']= 200
        context={
            'arbitro':arbitro,
            'tipo':"deleted",
        }
        data['content']= render_to_string('ajax/BTArbitros.html',context,request=request)

    else:
        # print "get delete form"
        data['status']= 200
        context={
            'arbitro':arbitro,
            'user':user,
            'arbitro':arbitro,
            'tipo':"delete",
        }
        data['content']= render_to_string('ajax/BTArbitros.html',context,request=request)
    return JsonResponse(data)


@login_required
def adminRemoveSubarea(request,id,subarea):
    print "Eliminar Subarea ", id
    
    data= dict()
    query= "SELECT * FROM main_app_usuario_asovac_sub_area AS usu_sub_a INNER JOIN main_app_sub_area AS sub_a on sub_a.id = usu_sub_a.sub_area_id "
    where=' WHERE usu_sub_a.id=%s ' 
    query= query+where
    query_result= Usuario_asovac.objects.raw(query,[subarea])

    # Para contar subareas 
    query='SELECT * FROM arbitrajes_arbitro AS arb INNER JOIN '+'"arbitrajes_arbitro_Sistema_asovac"'+' as sis_aso on sis_aso.arbitro_id = arb.id INNER JOIN main_app_usuario_asovac as usu_aso on usu_aso.id = arb.usuario_id INNER JOIN main_app_usuario_asovac_sub_area as usu_sub_a on usu_sub_a.usuario_asovac_id = usu_aso.id INNER JOIN main_app_sub_area as sub_a on sub_a.id = usu_sub_a.sub_area_id INNER JOIN main_app_area as ar on ar.id= sub_a.area_id'
    where=' WHERE usu_aso.id=%s ' 
    query= query+where
    total_subarea= Usuario_asovac.objects.raw(query,[id])
    
    total=0
    for item in total_subarea:
        total=total+1

    for item in query_result:
        subarea={'id':item.id,'nombre': item.nombre }

    if request.method == 'POST':

        print "para eliminar subarea total: ", total
        if total > 1:
            query= "DELETE FROM main_app_usuario_asovac_sub_area "
            where="WHERE id={}".format(subarea['id'])
            query= query+where
            # query_result= Usuario_asovac.objects.raw(query,[subarea['id']])
            
            cursor = connection.cursor()
            cursor.execute(query)
        
            data['status']= 200
            data['message']="La subárea se ha eliminado de forma exitosa."
        else:
            data['status']= 200
            data['message']="El árbitro debe tener almenos 1 subárea asociada."

    else:

        data['status']= 200
        context={
            'tipo':"removeSubareaArbitro",
            'id':id,
            'subarea':subarea,
        }
        data['content']= render_to_string('ajax/BTArbitros.html',context,request=request)
    return JsonResponse(data)

@login_required
def adminAddSubareas(request,id):
    print "ID recibido para agregar areas",id
    data= dict()
    user= get_object_or_404(User,id=id)
    auth_user=user    
    user= Usuario_asovac.objects.get(usuario_id=id)
    
    subareas= Sub_area.objects.all()
    subareas_user= user.sub_area.all()
    area= subareas_user.first().area
    array_subareas=[]

    for item in subareas_user:
        array_subareas.append(item.id)

    # print array_subareas
    # print subareas[0].area_id
    # print subareas_user[0].nombre
    # print area.id

    if request.method == 'POST':
        print "El metodo es post de add"
        subareas_post= request.POST.getlist("id")
        print (subareas_post)
        print (id)
        usuario_asovac= Usuario_asovac.objects.get(id=id)
        print usuario_asovac.id
        # Para eliminar registros viejos
        query= "DELETE FROM main_app_usuario_asovac_sub_area "
        where="WHERE usuario_asovac_id={}".format(usuario_asovac.id)
        query= query+where
        cursor = connection.cursor()
        cursor.execute(query)

        for item in subareas_post:
            array_subareas= item.split(',')
    
        # Para agregar nuevos registros
        for item in array_subareas:
            query= "INSERT INTO  main_app_usuario_asovac_sub_area (usuario_asovac_id, sub_area_id) VALUES "
            values="({0},{1})".format(id,item)
            
            query= query+values
            cursor = connection.cursor()
            cursor.execute(query)



        data['status']=200
        data['message']= "Se han actualizado las subáreas de forma exitosa."

    else:
        # print "el metodo es get"
        context= {
            'tipo': 'addSubareaArbitro',
            'area': area,
            'subareas':subareas,
            'subareas_user':array_subareas,
            'user_id': id,
        }
        data['content']=render_to_string('ajax/BTArbitros.html',context,request=request)

    return JsonResponse(data)

@login_required
def adminChangeAreas(request,id):
    print "ID recibido para agregar areas",id
    data= dict()
    user= get_object_or_404(User,id=id)
    auth_user=user    
    user= Usuario_asovac.objects.get(usuario_id=id)
    
    subareas= Sub_area.objects.all()
    areas= Area.objects.all()

    if request.method == 'POST':
        print "El metodo es post para cambiar de area"
        subareas_post= request.POST.getlist("subareas_value")
        # print (subareas_post)
        print request.POST.getlist("areas_value")
        print request.POST.getlist("subareas_value")
        # print (id)
        usuario_asovac= Usuario_asovac.objects.get(id=id)
        # print usuario_asovac.id
        # # Para eliminar registros viejos
        query= "DELETE FROM main_app_usuario_asovac_sub_area "
        where="WHERE usuario_asovac_id={}".format(usuario_asovac.id)
        query= query+where
        cursor = connection.cursor()
        cursor.execute(query)
        
        array_subareas=subareas_post
        
        # # Para agregar nuevos registros
        for item in array_subareas:
            query= "INSERT INTO  main_app_usuario_asovac_sub_area (usuario_asovac_id, sub_area_id) VALUES "
            values="({0},{1})".format(id,item)
            
            query= query+values
            cursor = connection.cursor()
            cursor.execute(query)

        data['status']=200
        data['message']= "Se han actualizado las subáreas de forma exitosa."

    else:
        # print "el metodo es get"
        context= {
            'tipo': 'changeAreaArbitro',
            'areas': areas,
            'subareas':subareas,
            'user_id': id,
        }
        data['content']=render_to_string('ajax/BTArbitros.html',context,request=request)

    return JsonResponse(data)


@login_required
def adminArea(request,id):
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

    

    context = {
        'nombre_vista' : 'Área árbitro',
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
        'user_id':id,
    }
    return render(request,"arbitrajes_admin_areas.html",context)

#---------------------------------------------------------------------------------#
#                            Carga la lista de subareas                           #
#---------------------------------------------------------------------------------#

@login_required
def getSubareas(request,id):
    print "Área seleccionada",id
    
    data= dict()
    subareas= Sub_area.objects.all().filter(area=id)

    data['status']=200

    context= {
        'subareas':subareas,
    }
    data['content']=render_to_string('ajax/load_subareas_arbitro.html',context,request=request)

    return JsonResponse(data)

#---------------------------------------------------------------------------------#
#                  Carga el contenido de la tabla de arbitraje                    #
#---------------------------------------------------------------------------------#
@login_required
def list_arbitrajes(request):
    
    event_id = request.session['arbitraje_id']
    rol_user=get_roles(request.user.id,event_id)
    user_area=get_area(request.user.id)

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
        limit= int(request.POST['limit'])+init
    
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
            query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
            query_count=query
            search= search+'%'
            where=" WHERE (trab.estatus like %s or trab.titulo_espanol like %s or trab.forma_presentacion like %s or trab.observaciones like %s or main_a.nombre like %s or main_sarea.nombre like %s ) AND sis_aso.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = true)) AND aut_trab.pagado=true AND trab.confirmacion_pago='Aceptado' "
            query= query+where
        else:
            if rol_user == 3:
                query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                query_count=query
                search= search+'%'
                where=" WHERE (trab.estatus like %s or trab.titulo_espanol like %s or trab.forma_presentacion like %s or trab.observaciones like %s or main_a.nombre like %s or main_sarea.nombre like %s ) AND sis_aso.id= %s AND main_a.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = true)) AND aut_trab.pagado=true AND trab.confirmacion_pago='Aceptado'"
                query= query+where
        if sort == "nombre":
            order_by="main_a."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
        else:
            order_by="trab."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
        query= query + " ORDER BY " + order_by
        if rol_user == 1 or rol_user ==2 :
            data= User.objects.raw(query,[search,search,search,search,search,search,event_id])
            data_count= User.objects.raw(query,[search,search,search,search,search,search,event_id])
            # data_count= User.objects.raw(query_count)
        else:
            if rol_user == 3:
                area= str(user_area.id)
                data= User.objects.raw(query,[search,search,search,search,search,search,event_id,area])
                data_count= User.objects.raw(query,[search,search,search,search,search,search,event_id,area])

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
                query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                where=" WHERE sis_aso.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true AND trab.confirmacion_pago='Aceptado' "
                query= query+where
            else:
                if rol_user == 3:
                    query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                    where=" WHERE sis_aso.id= %s AND main_a.id = %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true AND trab.confirmacion_pago='Aceptado' "
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
                    area= str(user_area.id)
                    data= User.objects.raw(query,[event_id,area])
                    data_count= User.objects.raw(query_count,[event_id,area])
           
            total=0
            for item in data_count:
                total=total+1
  
            # data= Usuario_asovac.objects.select_related('arbitro','usuario').filter( id=27).order_by(order)
            # total= len(data)

    # for item in data:
        # print("%s is %s. and total is %s" % (item.username, item.first_name,item.last_name, item.email))
        # response['query'].append({'id':item.id,'first_name': item.first_name,'last_name':item.last_name,'username': item.username,'email':item.email})

    for item in data:

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

        if item.estatus == "Aceptado":
            estatus= '<span class="label label-success">'+item.estatus +'</span>'
        else:
            if item.estatus == "Rechazado":
                estatus= '<span class="label label-danger">'+item.estatus +'</span>'
            else:
                estatus= '<span class="label label-warning">'+item.estatus +'</span>'

        titulo= item.titulo_espanol
        presentacion= item.forma_presentacion 
        observaciones = item.observaciones
        # autor_principal=item.nombres+' '+item.apellidos
        autor_principal=list_autores
        area = item.nombre
        subarea=item.subarea

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
    
        response['query'].append({'id':item.id,'estatus': estatus ,'nombre':area,'titulo_espanol':titulo ,'forma_presentacion':presentacion, 'observaciones':observaciones,'revision':revision, 'autor_principal':autor_principal,'subarea':subarea })


    response={
        'total': total,
        'query': response,
    }
   
    return JsonResponse(response)



#---------------------------------------------------------------------------------#
#                                CRUD de Arbitrajes                               #
#---------------------------------------------------------------------------------#
@login_required
def viewArbitraje(request, id):
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

    trabajo = Trabajo.objects.get( id = id)
    area=trabajo.subareas.all()[0].area.nombre
    subarea=trabajo.subareas.all()[0].nombre

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
        'area':area,
        'subarea':subarea,
        'trabajo':trabajo,
    }
    return render(request,"arbitrajes_trabajo_info.html",context)



@login_required
def changeStatus(request, id):
    
    response= dict()
    print "Cambio de estatus del trabajo"
    # Detalle del trabajo
    trabajo = Trabajo.objects.get( id = id)
    area=trabajo.subareas.all()[0].area.nombre
    subarea=trabajo.subareas.all()[0].nombre
    

    if request.method == 'POST':
        
        print "El metodo es post"
        print "Parametros enviados"

        try:
            
            if request.POST.get("status") == "Rechazado":
                # Para obtener el resultado de las evaluaciones
                query= "SELECT ta.* FROM trabajos_trabajo AS t INNER JOIN trabajos_trabajo_arbitro AS ta ON ta.trabajo_id=t.id INNER JOIN arbitrajes_arbitro AS a ON a.id= ta.arbitro_id"
                where=' WHERE t.id= %s '
                query= query+where

                data= Trabajo.objects.raw(query,[id])

                for arbitraje in data:
                    arbitraje_result=Trabajo_arbitro.objects.get(id=arbitraje.id)
                    if arbitraje.fin_arbitraje == False:
                        arbitraje_result.fin_arbitraje= True
                        arbitraje_result.save()

                trabajo.estatus=request.POST.get("status")
                trabajo.observaciones=request.POST.get("comment").strip()

            else:
                status=request.POST.get("status")
                if status == "Aceptado":
                    # Para obtener el resultado de las evaluaciones
                    query= "SELECT ta.* FROM trabajos_trabajo AS t INNER JOIN trabajos_trabajo_arbitro AS ta ON ta.trabajo_id=t.id INNER JOIN arbitrajes_arbitro AS a ON a.id= ta.arbitro_id"
                    where=' WHERE t.id= %s '
                    query= query+where

                    data= Trabajo.objects.raw(query,[id])

                    for arbitraje in data:
                        arbitraje_result=Trabajo_arbitro.objects.get(id=arbitraje.id)
                        if arbitraje.fin_arbitraje == False:
                            arbitraje_result.fin_arbitraje= True
                            arbitraje_result.save()

                trabajo.estatus=request.POST.get("status")
                trabajo.observaciones=""

            trabajo.save()
            response['status']= 200
            response['message']= "El estatus se ha cambiado de manera exitosa."
        except:
            response['status']= 400
            response['message']= "No se ha podido cambiar el estatus del trabajo."
            
    else:
       
        response['status']= 200
        context={
            'tipo':"changeStatus",
            'area':area,
            'subarea':subarea,
            'trabajo':trabajo,
            'trabajo_id':id,
        }
        response['content']= render_to_string('ajax/BTArbitrajes.html',context,request=request)
    
    return JsonResponse(response)



@login_required
def statusArbitraje(request, id):
    
    response= dict()
    # print "Estatus del arbitraje por parte de los arbitros"
    query= "SELECT t.id,a.correo_electronico, a.nombres, a.apellidos, ta.arbitraje_resultado, ta.comentario_autor FROM trabajos_trabajo AS t INNER JOIN trabajos_trabajo_arbitro AS ta ON ta.trabajo_id=t.id INNER JOIN arbitrajes_arbitro AS a ON a.id= ta.arbitro_id"
    where=' WHERE t.id= %s '
    query= query+where

    resultados=[]

    data= Trabajo.objects.raw(query,[id])
    for arbitraje in data:
        resultados.append({'id':arbitraje.id,'nombres': arbitraje.nombres,'apellidos':arbitraje.apellidos, 'correo_electronico':arbitraje.correo_electronico, 'evaluacion':arbitraje.arbitraje_resultado, 'comentario':arbitraje.comentario_autor  })
       
    response['status']= 200
    context={
        'tipo':"statusArbitraje",
        'arbitrajes':resultados,
    }
    response['content']= render_to_string('ajax/BTArbitrajes.html',context,request=request)
    
    return JsonResponse(response)



@login_required
def newArbitraje(request, id):

    trabajo= Trabajo.objects.get(id = id)
    trabajo.requiere_arbitraje=True
    trabajo.save()
    
    response= dict()
    response['status']= 200
    context={
        'tipo':"newArbitraje",
    }
    response['content']= render_to_string('ajax/BTArbitrajes.html',context,request=request)
    
    return JsonResponse(response)



#---------------------------------------------------------------------------------#
#             Carga el contenido para asignar sesiones a los trabajos             #
#---------------------------------------------------------------------------------#
@login_required
def list_trabajos_aceptados(request):

    event_id = request.session['arbitraje_id']
    rol_user=get_roles(request.user.id,event_id)
    user_area=get_area(request.user.id)

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
        limit= int(request.POST['limit'])+init
    
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
            query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,aut.nombres,aut.apellidos,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
            query_count=query
            search= search+'%'
            where=' WHERE (trab.estatus like %s or trab.titulo_espanol like %s or trab.forma_presentacion like %s or trab.observaciones like %s or main_a.nombre like %s or main_sarea.nombre like %s ) AND sis_aso.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = true)) AND aut_trab.pagado=true AND trab.estatus='+"'Aceptado' "
            query= query+where
        else:
            if rol_user == 3:
                query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,aut.nombres,aut.apellidos,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                query_count=query
                search= search+'%'
                where=' WHERE (trab.estatus like %s or trab.titulo_espanol like %s or trab.forma_presentacion like %s or trab.observaciones like %s or main_a.nombre like %s or main_sarea.nombre like %s ) AND sis_aso.id= %s AND main_a.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = true)) AND aut_trab.pagado=true AND trab.estatus='+"'Aceptado' "
                query= query+where
        if sort == "nombre":
            order_by="main_a."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
        else:
            order_by="trab."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
        query= query + " ORDER BY " + order_by
        if rol_user == 1 or rol_user ==2 :
            data= User.objects.raw(query,[search,search,search,search,search,search,event_id])
            data_count= User.objects.raw(query,[search,search,search,search,search,search,event_id])
            # data_count= User.objects.raw(query_count)
        else:
            if rol_user == 3:
                area= str(user_area.id)
                data= User.objects.raw(query,[search,search,search,search,search,search,event_id,area])
                data_count= User.objects.raw(query,[search,search,search,search,search,search,event_id,area])

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
                query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,aut.nombres,aut.apellidos,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                where=" WHERE sis_aso.id= %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true AND trab.estatus='Aceptado' AND trab.confirmacion_pago='Aceptado' "
                query= query+where
            else:
                if rol_user == 3:
                    query= "SELECT DISTINCT(trab.id),trab.estatus,trab.requiere_arbitraje,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones,aut.nombres,aut.apellidos,main_sarea.nombre as subarea FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                    where=" WHERE sis_aso.id= %s AND main_a.id = %s AND ((trab.requiere_arbitraje = false) or (trab.padre<>0 and trab.requiere_arbitraje = false)) AND aut_trab.pagado=true AND trab.estatus='Aceptado' AND trab.confirmacion_pago='Aceptado' "
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
                    area= str(user_area.id)
                    data= User.objects.raw(query,[event_id,area])
                    data_count= User.objects.raw(query_count,[event_id,area])
           
            total=0
            for item in data_count:
                total=total+1
  
            # data= Usuario_asovac.objects.select_related('arbitro','usuario').filter( id=27).order_by(order)
            # total= len(data)

    # for item in data:
        # print("%s is %s. and total is %s" % (item.username, item.first_name,item.last_name, item.email))
        # response['query'].append({'id':item.id,'first_name': item.first_name,'last_name':item.last_name,'username': item.username,'email':item.email})

    for item in data:

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


        if item.estatus == "Aceptado":
            estatus= '<span class="label label-success">'+item.estatus +'</span>'
        else:
            if item.estatus == "Rechazado":
                estatus= '<span class="label label-danger">'+item.estatus +'</span>'
            else:
                estatus= '<span class="label label-warning">'+item.estatus +'</span>'

        titulo= item.titulo_espanol
        presentacion= item.forma_presentacion 
        observaciones = item.observaciones
        # autor_principal=item.nombres+' '+item.apellidos
        autor_principal=list_autores
        area = item.nombre
        subarea=item.subarea
        
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
    
        response['query'].append({'id':item.id,'estatus': estatus ,'nombre':area,'titulo_espanol':titulo ,'forma_presentacion':presentacion, 'observaciones':observaciones,'revision':revision, 'autor_principal':autor_principal,'subarea':subarea })


    response={
        'total': total,
        'query': response,
    }
   
    return JsonResponse(response)
    


#---------------------------------------------------------------------------------#
#                          CRUD Trabajos Aceptados                                #
#---------------------------------------------------------------------------------#
@login_required
def editPresentacion(request,id):
    print "Edit Presentacion"
    data= dict()

    if request.method == 'POST':

        trabajo= Trabajo.objects.get(id = id)
        trabajo.forma_presentacion=request.POST.get("forma_presentacion")
        trabajo.save()
        
        data['status']= 200
        data['message']="La forma de presentación se ha cambiado de manera exitosa."

    else:

        data['status']= 200
        context={
            'tipo':"editPresentacion",
            'trabajo_id':id,
        }
        data['content']= render_to_string('ajax/BTArbitrajes.html',context,request=request)
    return JsonResponse(data)

@login_required
def asigSesion(request,id):
    print "Asignar sesión"
    data= dict()
    arbitraje = request.session['arbitraje_id']
    listSesion= Sesion.objects.filter(sistema=arbitraje)
    trabajo= Trabajo.objects.get(id = id)
    print trabajo.sesion_id

    if request.method == 'POST':

        sesion=Sesion.objects.get(id=request.POST.get("sesion")) 
        # trabajo= Trabajo.objects.get(id = id)
        trabajo.sesion= sesion
        trabajo.save()
        
        data['status']= 200
        data['message']="La forma de presentación se ha cambiado de manera exitosa."

    else:

        data['status']= 200
        context={
            'tipo':"asigSesion",
            'trabajo_id':id,
            'asig': trabajo.sesion_id,
            'sesiones': listSesion,
        }
        data['content']= render_to_string('ajax/BTArbitrajes.html',context,request=request)
    return JsonResponse(data)

#---------------------------------------------------------------------------------#
#                               Exportar Arbitro                                  #
#---------------------------------------------------------------------------------#
@login_required
def generate_report(request,tipo):
    print "Excel para arbitros"
    event_id = request.session['arbitraje_id']
    rol_user=get_roles(request.user.id,event_id)
    user_area=get_area(request.user.id)
    # Para exportar información de Arbitro
    if tipo == '1':
        # consulta para obtener informacion de los Arbitros
        # query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id"
        # Consulta según rol de usuario
        if rol_user == 1 or rol_user == 2:
                query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS asa ON asa.arbitro_id = arb.id"
        else:
            if rol_user == 3:
                query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS asa ON asa.arbitro_id = arb.id"
                where=' WHERE a.id=  %s '
                query= query+where

        # query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id"
        query_count=query
        query= query

        # data= User.objects.raw(query)
        # data_count= User.objects.raw(query_count)

        if rol_user == 1 or rol_user ==2 :
                data= User.objects.raw(query)
                data_count= User.objects.raw(query_count)
        else:
            if rol_user == 3:
                area= str(user_area.id)
                data= User.objects.raw(query,area)
                data_count= User.objects.raw(query_count,area)

        total=0
        for item in data_count:
            total=total+1

        # Para definir propiedades del documento de excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Arbitros.xls'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet("Usuarios")
        # Para agregar los titulos de cada columna
        row_num = 0
        columns = ['Nombres (*)', 'Apellidos (*)', 'Nombre de usuario (*)','Correo electronico (*)','Área (*)','Subarea 1 (*)','Subarea 2','Subarea 3','Género (*)','Cédula o pasaporte (*)','Título (*)','Línea de investigación (*)','Teléfono oficina','Teléfono celular o habitación (*)','Institución donde  trabaja','Datos de la institución','Observaciones']
        for col_num in range(len(columns)):
            worksheet.write(row_num, col_num, columns[col_num])

        for item in data:
            row_num += 1
            row = [item.first_name ,item.last_name ,item.username ,item.email,item.nombre,'-','-','-',item.genero,item.cedula_pasaporte,item.titulo,item.linea_investigacion,'-','-','-','-','-']
            for col_num in range(len(row)):
                worksheet.write(row_num, col_num, row[col_num])

        workbook.save(response)

    return response



@login_required
def review_job(request, trabajo_id):
    data = dict()
    trabajo = Trabajo.objects.get(id = trabajo_id)
    if request.method == "POST":
        status = request.POST.get("status")
        observation = request.POST.get("comment")
        print observation
        usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
        arbitro = Arbitro.objects.get(usuario = usuario_asovac)
        trabajo_arbitro = Trabajo_arbitro.objects.get(trabajo = trabajo, arbitro = arbitro)
        trabajo_arbitro.fecha_arbitraje = date.today().isoformat()
        trabajo_arbitro.fin_arbitraje = True
        trabajo_arbitro.arbitraje_resultado = status
        if status == "Rechazado":
            trabajo_arbitro.comentario_autor = observation
        trabajo_arbitro.save()
        messages.success(request,"El trabajo fue arbitrado con éxito.")
        return redirect('arbitrajes:jobs_for_review')
    else:
        context = {
            'trabajo': trabajo,
        }
        data['html_form'] = render_to_string('ajax/review_job.html',context,request=request)
    return JsonResponse(data)