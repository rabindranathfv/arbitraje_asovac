# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.core.mail import send_mail
from django.shortcuts import render

import random, string,xlrd,os,sys,xlwt
from main_app.models import Rol,Sistema_asovac,Usuario_asovac
from .models import Arbitro
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status, get_area,exist_email
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template.loader import render_to_string

from .forms import ArbitroForm

from .models import Arbitro

# Create your views here.
def arbitrajes_pag(request):
    context = {
        "nombre_vista": 'Arbitrajes'
    }
    return render(request,"test_views.html",context)


def listado_trabajos(request):

    estado = request.session['estado']
    event_id = request.session['arbitraje_id']
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
        'nombre_vista' : 'Listado de Trabajos',
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
    return render(request, 'arbitrajes_trabajos_list.html', context)

def detalles_resumen(request):
    context = {
        'nombre_vista' : 'Detalles de Resumen',
    }
    return render(request, 'arbitrajes_detalle_resumen.html', context)

def referee_list(request):

    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']
    rol_id=get_roles(request.user.id,arbitraje_id)

    item_active = 2
    items=validate_rol_status(estado,rol_id,item_active, arbitraje_id)

    route_conf= get_route_configuracion(estado,rol_id, arbitraje_id)
    route_seg= get_route_seguimiento(estado,rol_id)
    route_trabajos_sidebar = get_route_trabajos_sidebar(estado,rol_id,item_active)
    route_trabajos_navbar = get_route_trabajos_navbar(estado,rol_id)
    route_resultados = get_route_resultados(estado,rol_id, arbitraje_id)

    referee_data = Arbitro.objects.all().order_by('-id')

    context = {
        'nombre_vista' : 'Listado de Arbitros',
        'estado' : estado,
        'rol_id' : rol_id,
        'arbitraje_id' : arbitraje_id,
        'item_active' : item_active,
        'items':items,
        'referee_data': referee_data,
        'route_conf':route_conf,
        'route_seg':route_seg,
        'route_trabajos_sidebar':route_trabajos_sidebar,
        'route_trabajos_navbar': route_trabajos_navbar,
        'route_resultados': route_resultados,
    }
    return render(request, 'arbitrajes_referee_list.html', context)

def referee_edit(request):

    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']
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
    return render(request, 'arbitrations_areas_subareas.html', context)


def asignacion_de_sesion(request):

    estado = request.session['estado']
    event_id = request.session['arbitraje_id']
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
        'nombre_vista' : 'Asignar Sesiónes | Lista de Árbitros según Subáreas',
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
                    query= "SELECT DISTINCT ua.usuario_id, au.first_name,au.last_name, au.email,ua.id, au.username, a.nombre, arb.genero, arb.cedula_pasaporte,arb.titulo, arb.linea_investigacion, arb.telefono_habitacion_celular FROM main_app_usuario_asovac AS ua INNER JOIN auth_user AS au ON ua.usuario_id = au.id INNER JOIN main_app_usuario_asovac_sub_area AS uasa ON uasa.usuario_asovac_id= ua.id INNER JOIN main_app_sub_area AS sa ON sa.id= uasa.sub_area_id INNER JOIN main_app_area AS a ON a.id = sa.area_id INNER JOIN main_app_usuario_rol_in_sistema AS ris ON ris.usuario_asovac_id = ua.id INNER JOIN arbitrajes_arbitro AS arb ON arb.usuario_id = ua.id INNER JOIN "+'"arbitrajes_arbitro_Sistema_asovac"'+" AS asa ON asa.arbitro_id = arb.id"
                    where=' WHERE a.id=  %s '
                    query= query+where
            
            order_by="au."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
            query_count=query
            query= query + " ORDER BY " + order_by
            
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
#                                 Crud Arbitros                                   #
#---------------------------------------------------------------------------------#
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

#---------------------------------------------------------------------------------#
#                               Exportar Arbitro                                 #
#---------------------------------------------------------------------------------#
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

