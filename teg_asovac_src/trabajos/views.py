# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404, redirect

#import settings
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse

from .models import Trabajo, Detalle_version_final
from autores.models import Autor, Autores_trabajos
from autores.forms import AddAuthorToJobForm

from main_app.models import Rol,Sistema_asovac,Usuario_asovac,User, Area, Sub_area, Usuario_rol_in_sistema
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status

from .forms import TrabajoForm,EditTrabajoForm, AutorObservationsFinalVersionJobForm
#Vista donde están la lista de trabajos del autor y dónde se le permite crear, editar o eliminar trabajos
def trabajos(request):
    form = TrabajoForm()
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
   
    # print (rol_id)
    
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


    usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
    autor = Autor.objects.get(usuario = usuario_asovac)
    sistema_asovac = Sistema_asovac.objects.get(id = arbitraje_id)

    # print items
    if request.method =='POST':
        form = TrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            new_trabajo = form.save()

            #Código para crear una instancia de Autores_trabajos
            autor_trabajo = Autores_trabajos(autor = autor, trabajo = new_trabajo, es_autor_principal = True, es_ponente = True, sistema_asovac = sistema_asovac)
            autor_trabajo.save()


    trabajos_list = Autores_trabajos.objects.filter(autor = autor, sistema_asovac = sistema_asovac)

#   for trabajo in trabajos:
#       print(trabajo.trabajo.titulo_espanol)
    paginator = Paginator(trabajos_list, 10) #Muestra 10 trabajos por página

    page = request.GET.get('page')

    try:
        trabajos = paginator.page(page)
    except PageNotAnInteger:
        #Si la página no es un entero, retorna la primera página
        trabajos = paginator.page(1)
    except EmptyPage:
        trabajos = paginator.page(paginator.num_pages)


    autores_trabajos_list = Autores_trabajos.objects.filter(sistema_asovac = sistema_asovac)

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
        'autores_trabajos_list': autores_trabajos_list,
    }
    return render(request,"trabajos.html",context)

def jobs_list(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    # request.session para almacenar el item seleccionado del sidebar
    request.session['sidebar_item'] = "Trabajos"

    estado = request.session['estado']
    arbitraje_id = request.session['arbitraje_id']
    rol_id=get_roles(request.user.id,arbitraje_id)

    # Seción para obtener área y subarea enviada por sesión y filtrar consulta
    area=request.session['area']
    subarea=request.session['subarea']
    # print "Area y Subarea enviadas por sesion"
    # print area
    # print subarea
    trabajos=Trabajo.objects.all().filter( Q(subarea1=subarea) | Q(subarea2=subarea) | Q(subarea3=subarea) )

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

def jobs_edit(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]



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
   

# Vista para editar trabajos
def edit_trabajo(request, trabajo_id):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


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
    usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
    autor = Autor.objects.get(usuario = usuario_asovac)
    trabajo = Trabajo.objects.get( id = trabajo_id)
    autor_trabajo = get_object_or_404(Autores_trabajos,  trabajo = trabajo, autor = autor, sistema_asovac = arbitraje_id)

      
    if request.method == 'POST':
        form = EditTrabajoForm(request.POST, request.FILES, instance = autor_trabajo.trabajo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sus cambios al trabajo han sido guardados con éxito.')
            return redirect('trabajos:trabajos')
    else: 
        form = EditTrabajoForm(instance = autor_trabajo.trabajo)


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
    }
    return render(request,"trabajos_edit_trabajo.html",context)

#Vista donde aparecen los trabajos evaluados
def trabajos_evaluados(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


    estado = request.session['estado']
    event_id = request.session['arbitraje_id']
    rol_id=get_roles(request.user.id,arbitraje_id)

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

def detalles_trabajo(request, trabajo_id):
    main_navbar_options = [{'title':'Configuración','icon': 'fa-cogs','active': True },
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


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
    usuario_asovac = Usuario_asovac.objects.get(usuario = request.user)
    autor = Autor.objects.get(usuario = usuario_asovac)
    trabajo = Trabajo.objects.get( id = trabajo_id)
    autor_trabajo = get_object_or_404(Autores_trabajos,  trabajo = trabajo, autor = autor, sistema_asovac = arbitraje_id)

    print(autor_trabajo.trabajo.archivo_trabajo.url)

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
        'autor_trabajo':autor_trabajo,
    }
    return render(request,"trabajos_detalles.html",context)



def trabajos_resultados_autor(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': True},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]


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


def show_job_observations(request, trabajo_version_final_id):
    data = dict()
    trabajo_version_final = get_object_or_404(Detalle_version_final, id = trabajo_version_final_id)
    context = {
        'trabajo_version_final': trabajo_version_final,
    }
    data['html_form'] = render_to_string('ajax/job_observations.html',context, request=request)
    return JsonResponse(data)


def autor_add_observations_to_job(request, trabajo_version_final_id):
    data = dict()
    trabajo = get_object_or_404(Detalle_version_final, id = trabajo_version_final_id)
    if request.method == "POST":
        form = AutorObservationsFinalVersionJobForm(request.POST, instance = trabajo)
        form.save()
        messages.success(request,"La observación fue guardada con éxito.")
        return redirect('trabajos:trabajos_resultados_autor')
    else:
        form = AutorObservationsFinalVersionJobForm(instance = trabajo)
        context = {
            'trabajo_version_final': trabajo,
            'form':form,
        }
        data['html_form'] = render_to_string('ajax/autor_add_job_observations.html', context, request=request)
    return JsonResponse(data)


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
            new_autor_trabajo = Autores_trabajos(autor = autor, trabajo = autor_trabajo.trabajo, sistema_asovac = sistema_asovac ,es_autor_principal = False, es_ponente = form_data['es_ponente'], es_coautor = form_data['es_coautor'])
            new_autor_trabajo.save()
            rol_autor = Rol.objects.get(id=5)

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