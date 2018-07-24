# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .forms import MyLoginForm, CreateArbitrajeForm, RegisterForm, DataBasicForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from .models import Rol,Sistema_asovac,Usuario_asovac

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

    context = {
        'nombre_vista' : 'Home',
        'secondary_navbar_options' : secondary_navbar_options,
        'arb_context' : arbitraje_data,
    }
    return render(request, 'main_app_home.html', context)

def create_arbitraje(request):
    form = CreateArbitrajeForm()
    context = {
        'nombre_vista' : 'Crear Arbitraje',
        'username' : 'Rabindranath Ferreira',
        'form' : form,
    }
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


def dashboard(request,arb_id):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]
    print("DEBAJO ESTA EL USERNAME")
    print(request.user.username)
    # queryset del estado del proceso
    data = Sistema_asovac.objects.get(pk=arb_id)


    context = {
        'nombre_vista' : 'Dashboard',
        'main_navbar_options' : main_navbar_options,
        'estado' : data.estado_arbitraje,
        'item_active' : '1',
    }
    return render(request, 'main_app_dashboard.html', context)

def data_basic(request):
    form= DataBasicForm()

    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'username' : 'Username',
        'estado' : '0',
        'item_active' : '1',
        'form' : form
    }
    return render(request, 'main_app_data_basic.html', context)

def state_arbitration(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : '0',
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_status_arbitration.html', context)

def users_list(request):

    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : '0',
        'item_active' : '1',
        'username' : 'Username',
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

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : '0',
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_edit_user.html', context)

def user_roles(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : '0',
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_user_roles.html', context)

def coord_general(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : '0',
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_coord_general.html', context)

def coord_area(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : '0',
        'item_active' : '1',
        'username' : 'Username',
    }
    return render(request, 'main_app_coord_area.html', context)

def total(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': True},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'estado' : '0',
        'item_active' : '3',
        'username' : 'Username',
    }
    return render(request, 'main_app_totales.html', context)