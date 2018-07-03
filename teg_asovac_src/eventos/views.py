# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def eventos_pag(request):
    context = {
        "nombre_vista": 'Recursos'
    }
    return render(request,"test_views.html",context)