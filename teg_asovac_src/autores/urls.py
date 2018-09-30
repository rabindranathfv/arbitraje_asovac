"""web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.autores_pag, name= 'autores'),

    url(r'^listar-autores/$',views.authors_list,name='authors_list'),
    url(r'^editar-autores/$',views.author_edit,name='author_edit'),

    url(r'^generar-certificado/$', views.generar_certificado, name = 'generar_certificado'),
    url(r'^postular-trabajo/$', views.postular_trabajo, name= 'postular_trabajo'),
    url(r'^postular-trabajo/pagador/$', views.postular_trabajo_pagador, name= 'postular_trabajo_pagador'),
    url(r'^postular-trabajo/pago/$', views.postular_trabajo_pago, name= 'postular_trabajo_pago'),
    url(r'^postular-trabajo/factura/$', views.postular_trabajo_factura, name= 'postular_trabajo_factura'),
    url(r'^postular-trabajo/detalles-pago/(?P<pagador_id>\d+)/$', views.detalles_pago, name= 'detalles_pago'),
    url(r'^postular-trabajo/editar/datos-pagador/(?P<pagador_id>\d+)/$', views.editar_datos_pagador, name= 'editar_datos_pagador'),
    url(r'^postular-trabajo/editar/pago/(?P<pago_id>\d+)/$', views.editar_pago, name= 'editar_pago'),
    url(r'^postular-trabajo/editar/factura/(?P<factura_id>\d+)/$', views.editar_factura, name= 'editar_factura'),
    url(r'^postular-trabajo/editar/(?P<pagador_id>\d+)/$', views.postular_editar, name= 'postular_editar'),
]