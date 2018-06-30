# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import MyLoginForm

# Create your views here.
def login(request):
    form = MyLoginForm()
    context = {
        "nombre_vista" : 'Login',
        "form" : form,
    }
    return render(request, "login.html", context)

def dashboard(request):
    context = {
        "nombre_vista" : 'Administracion',
    }
    return render(request, "dashboard.html", context)
