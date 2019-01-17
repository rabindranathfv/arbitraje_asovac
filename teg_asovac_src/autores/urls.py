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


    url(r'^administrador/crear-autor/$',views.admin_create_author,name='admin_create_author'),
    url(r'^crear-universidad/$',views.create_university_modal, name='create_university_modal'),
    url(r'^listar-autores/$',views.authors_list,name='authors_list'),
    url(r'^editar-autor/(?P<autor_id>\d+)/$',views.author_edit,name='author_edit'),
    url(r'^detalles/(?P<autor_id>\d+)/$',views.author_details,name='author_details'),

    url(r'^generar-certificado/$', views.generar_certificado, name = 'generar_certificado'),
    
    url(r'^postular-trabajo/$', views.postular_trabajo, name= 'postular_trabajo'),

    url(r'^postular-trabajo/pagador/(?P<autor_trabajo_id>\d+)/$', views.postular_trabajo_pagador_modal, name= 'postular_trabajo_pagador_modal'),
    url(r'^postular-trabajo/factura/(?P<autor_trabajo_id>\d+)/$', views.postular_trabajo_factura_modal, name= 'postular_trabajo_factura_modal'),
    url(r'^postular-trabajo/pago/(?P<autor_trabajo_id>\d+)/$', views.postular_trabajo_pago_modal, name= 'postular_trabajo_pago_modal'),
    url(r'^editar-perfil/(?P<user_id>\d+)/$',views.author_edit_modal,name='author_edit_modal'),


    url(r'^postular-trabajo/detalles-pago/(?P<pagador_id>\d+)/$', views.detalles_pago, name= 'detalles_pago'),

    #Carga de contenido 
    url(r'^load-authors-data$',views.list_authors,name='list_authors'),
]