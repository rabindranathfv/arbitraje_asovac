# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
from .forms import DatosPagadorForm, PagoForm, FacturaForm
# Create your views here.
def generar_certificado(request):
	context={
		"nombre_vista": 'Generar Certificado'
	}
	return render(request,"autores_generar_certificado.html", context)

def postular_trabajo(request):
	pagadorform = DatosPagadorForm()
	pagoform = PagoForm()
	facturaform = FacturaForm()
	context = {
		"nombre_vista": 'Postular Trabajo',
		"pagadorform": pagadorform,
		"pagoform": pagoform,
		"facturaform": facturaform,
	}
	return render(request,"autores_postular_trabajo.html",context)

def postular_trabajo_pagador(request):
	pagadorform = DatosPagadorForm()
	context = {
		"nombre_vista": 'Postular Trabajo - Pagador',
		"pagadorform": pagadorform,
	}
	return render(request,"autores_postular_trabajo_pagador.html",context)

def postular_trabajo_pago(request):
	pagoform = PagoForm()
	context = {
		"nombre_vista": 'Postular Trabajo - Pago',
		"pagoform": pagoform,
	}
	return render(request,"autores_postular_trabajo_pago.html",context)

def postular_trabajo_factura(request):
	facturaform = FacturaForm()
	context = {
		"nombre_vista": 'Postular Trabajo - Factura',
		"facturaform": facturaform,
	}
	return render(request,"autores_postular_trabajo_factura.html",context)