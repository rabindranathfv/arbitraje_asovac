# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from .forms import TrabajoForm

def trabajos(request):
    form = TrabajoForm()
    context = {
        "nombre_vista": 'Autores',
        "form": form,
    }
    return render(request,"trabajos.html",context)

def edit_trabajo(request):
	form = TrabajoForm()
	context = {
		"nombre_vista": 'Editar Trabajo',
		"form": form,
    }
	return render(request,"trabajos_edit_trabajo.html",context)

def trabajos_evaluados(request):
	context = {
		"nombre_vista": 'Trabajos Evaluados'
	}
	return render(request,"trabajos_trabajos_evaluados.html",context)
