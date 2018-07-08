# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import MyLoginForm, CreateArbitrajeForm

# Create your views here.
def login(request):
    form = MyLoginForm()
    context = {
        'nombre_vista' : 'Login',
        'form' : form,
    }
    return render(request, 'login.html', context)

def home(request):
    secondary_navbar_options = ['Bienvenido']

    context = {
        'nombre_vista' : 'Home',
        'secondary_navbar_options' : secondary_navbar_options,
        'username' : 'Rabindranath Ferreira',
    }
    return render(request, 'home.html', context)

def create_arbitraje(request):
    form = CreateArbitrajeForm()
    context = {
        'nombre_vista' : 'Crear Arbitraje',
        'username' : 'Rabindranath Ferreira',
        'form' : form,
    }
    return render(request, 'create_arbitraje.html', context)


def dashboard(request):
    main_navbar_options = [{'title':'Configuración',   'icon': 'fa-cogs',      'active': True},
                    {'title':'Monitoreo',       'icon': 'fa-eye',       'active': False},
                    {'title':'Resultados',      'icon': 'fa-chart-area','active': False},
                    {'title':'Administración',  'icon': 'fa-archive',   'active': False}]

    secondary_navbar_options = ['Opciones Secundarias']

    context = {
        'nombre_vista' : 'Dashboard',
        'main_navbar_options' : main_navbar_options,
        'secondary_navbar_options' : secondary_navbar_options,
        'username' : 'Username',
    }
    return render(request, 'dashboard.html', context)
