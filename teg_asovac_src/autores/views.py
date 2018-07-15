# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from .forms import CreateTrabajoForm
# Create your views here.
def autores_pag(request):
    form = CreateTrabajoForm()
    context = {
        "nombre_vista": 'autores',
        "form": form,
    }
    return render(request,"autor.html",context)