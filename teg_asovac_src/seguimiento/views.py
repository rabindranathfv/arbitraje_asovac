# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def seguimiento_pag(request):
    context = {
        "nombre_vista": 'seguimiento'
    }
    return render(request,"test_views.html",context)