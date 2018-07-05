# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import MyLoginForm

# Create your views here.
def login(request):
    form = MyLoginForm()
    context = {
        'nombre_vista' : 'Login',
        'form' : form,
    }
    return render(request, 'login.html', context)

def home(request):
    main_navbar_options = [ {'title':'Configuración',   'icon': 'fa-cogs',      'active': False},
                            {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                            {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                            {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Bienvenido']

    context = {
        'nombre_vista' : 'Administración',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'username' : 'Rabindranath Ferreira',
    }
    return render(request, 'home.html', context)

def dashboard(request):
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
    }
    return render(request, 'dashboard.html', context)
