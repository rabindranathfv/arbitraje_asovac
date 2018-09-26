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
    # url(r'^trabajos/$', views.trabajos_pag, name= 'trabajos'),
    url(r'^listar-trabajos/$', views.jobs_list, name= 'jobs_list'),
    url(r'^editar-sesion/$', views.jobs_edit, name= 'jobs_edit'),
  
    url(r'^$', views.trabajos, name= 'trabajos'),
    url(r'^editar-trabajo/(?P<trabajo_id>\d+)/$', views.edit_trabajo, name= 'edit_trabajo'),
    url(r'^detalles/(?P<trabajo_id>\d+)/$', views.detalles_trabajo, name= 'detalles_trabajo'),
    url(r'^trabajos-evaluados/$', views.trabajos_evaluados, name = 'trabajos_evaluados'),
    url(r'^resultados/$', views.trabajos_resultados_autor, name = 'trabajos_resultados_autor'),

    # Ajax
    url(r'^eliminar/(?P<trabajo_id>\d+)/$',views.delete_job , name='delete_job'),
    url(r'^resultados/observaciones/(?P<trabajo_version_final_id>\d+)/$',views.show_job_observations , name='show_job_observations'),
]