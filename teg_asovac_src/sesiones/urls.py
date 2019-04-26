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
    url(r'^sesiones/$', views.sesiones_pag, name= 'sesiones'),
    url(r'^crear/$', views.create_sesion, name= 'create_sesion'),
    url(r'^lista/$', views.sesions_list, name= 'sesions_list'),
    url(r'^editar/(?P<sesion_id>\d+)$', views.edit_sesion, name= 'edit_sesion'),
    url(r'^espacio/lista/$', views.sesions_space_list, name= 'sesions_space_list'),
    url(r'^espacio/editar/$', views.sesions_space_edit, name= 'sesions_space_edit'),

    #Bootstrap Table data
    url(r'^load-sesions-data$',views.list_sesions,name='list_sesions'),

    #Ajax
    url(r'^cargar-espacio-form/(?P<modalidad>\d+)$', views.load_space_form, name= 'load_space_form'),
    url(r'^eliminar/(?P<sesion_id>\d+)$', views.delete_sesion, name= 'delete_sesion'),
    url(r'^detalles/(?P<sesion_id>\d+)$', views.details_sesion, name= 'details_sesion'),
    url(r'^lista-trabajos/(?P<sesion_id>\d+)$', views.sesion_job_list, name= 'sesion_job_list'),
    url(r'^(?P<sesion_id>\d+)/asignar-coordinador/(?P<autor_id>\d+)$', views.assign_coordinator, name= 'assign_coordinator'),
    
]