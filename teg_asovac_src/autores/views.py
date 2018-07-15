# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from .forms import TrabajoForm
# Create your views here.
def autores_pag(request):
    form = TrabajoForm()
    context = {
        "nombre_vista": 'Autores',
        "form": form,
    }
    return render(request,"autor.html",context)

def edit_trabajo(request):
	form = TrabajoForm()
	context = {
		"nombre_vista": 'Editar Trabajo',
		"form": form,
    }
	return render(request,"autor-editar-trabajo.html",context)