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
from main_app.views import get_route_resultados, get_route_trabajos_navbar, get_route_trabajos_sidebar, get_roles, get_route_configuracion, get_route_seguimiento, validate_rol_status, get_area,exist_email
from .forms import TrabajoForm,EditTrabajoForm, AutorObservationsFinalVersionJobForm
#Vista donde están la lista de trabajos del autor y dónde se le permite crear, editar o eliminar trabajos
def trabajos(request):
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
        subarea_list = request.POST.getlist("subarea_select")
        if form.is_valid() and len(subarea_list) <= 3:
            new_trabajo = form.save()
            counter = 0
            for subarea in subarea_list:
                area_to_assign = Sub_area.objects.get(id = subarea)
                new_trabajo.subareas.add(area_to_assign)

            new_trabajo.save()

            #Código para crear una instancia de Autores_trabajos
            autor_trabajo = Autores_trabajos(autor = autor, trabajo = new_trabajo, es_autor_principal = True, es_ponente = True, sistema_asovac = sistema_asovac, monto_total = sistema_asovac.monto_pagar_trabajo)
            autor_trabajo.save()
            form = TrabajoForm()
        else:
            if(3 < len(subarea_list)):
                messages.error(request,"Solo puede elegir hasta 3 subareas al momento de crear un trabajo.")
    else:
        form = TrabajoForm()

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
    areas= Area.objects.all()
    subareas= Sub_area.objects.all()
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
        'areas':areas,
        'subareas':subareas
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
        subarea_list = request.POST.getlist("subarea_select")
        area= request.POST.get("area_select")
        if (form.is_valid() and (not area or (subarea_list and len(subarea_list) <= 3))):
            trabajo_edit = form.save()
            if(area): 
                new_area = Area.objects.get(id = area)
                trabajo_edit.area = new_area
                trabajo_edit.subareas.clear()
                
                for subarea in subarea_list:
                    new_subarea = Sub_area.objects.get(id = subarea)
                    trabajo_edit.subareas.add(new_subarea)

                
                trabajo_edit.save()


            messages.success(request, 'Sus cambios al trabajo han sido guardados con éxito.')
            return redirect('trabajos:trabajos')
        else:
            if (3 < len(subarea_list)):
                messages.error(request, 'Solo puede elegir hasta 3 subáreas.')
                
    else: 
        form = EditTrabajoForm(instance = autor_trabajo.trabajo)

    areas= Area.objects.all()
    subareas= Sub_area.objects.all()
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
        'subareas':subareas
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

def list_trabajos(request):
    
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
            query= "SELECT DISTINCT(trab.id),trab.estatus,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
            query_count=query
            search= search+'%'
            where=' WHERE trab.estatus like %s or trab.titulo_espanol like %s or trab.forma_presentacion like %s or trab.observaciones like %s or main_a.nombre like %s '
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
        if sort == "nombre":
            order_by="main_a."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
        else:
            order_by="trab."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
        query= query + " ORDER BY " + order_by
        if rol_user == 1 or rol_user ==2 :
            data= User.objects.raw(query,[search,search,search,search,search])
            data_count= User.objects.raw(query,[search,search,search,search,search])
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
                query= "SELECT DISTINCT(trab.id),trab.estatus,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
            else:
                if rol_user == 3:
                    query= "SELECT DISTINCT(trab.id),trab.estatus,trab.titulo_espanol,trab.forma_presentacion,main_a.nombre,trab.observaciones FROM trabajos_trabajo AS trab INNER JOIN autores_autores_trabajos AS aut_trab ON aut_trab.trabajo_id = trab.id INNER JOIN autores_autor AS aut ON aut.id = aut_trab.autor_id INNER JOIN main_app_sistema_asovac AS sis_aso ON sis_aso.id = aut_trab.sistema_asovac_id INNER JOIN trabajos_trabajo_subareas AS trab_suba ON trab_suba.trabajo_id = trab.id INNER JOIN main_app_sub_area AS main_sarea on main_sarea.id = trab_suba.sub_area_id INNER JOIN main_app_area AS main_a ON main_a.id= main_sarea.area_id"
                    where=' WHERE main_a.id= %s '
                    query= query+where
            
            if sort=="nombre":
                order_by="main_a."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
            else:
                order_by="trab."+ str(sort)+ " " + order + " LIMIT " + str(limit) + " OFFSET "+ str(init) 
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

            # print data
            total=0
            for item in data_count:
                total=total+1
  
            # data= Usuario_asovac.objects.select_related('arbitro','usuario').filter( id=27).order_by(order)
            # total= len(data)

    # for item in data:
        # print("%s is %s. and total is %s" % (item.username, item.first_name,item.last_name, item.email))
        # response['query'].append({'id':item.id,'first_name': item.first_name,'last_name':item.last_name,'username': item.username,'email':item.email})
    
    for item in data:
        estatus= item.estatus 
        titulo= item.titulo_espanol
        presentacion= item.forma_presentacion 
        observaciones = item.observaciones
        area = item.nombre
        response['query'].append({'id':item.id,'estatus': estatus ,'nombre':area,'titulo_espanol':titulo ,'forma_presentacion':presentacion, 'observaciones':observaciones  })


    response={
        'total': total,
        'query': response,
    }
   
    return JsonResponse(response)
