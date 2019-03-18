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
    url(r'^listado-trabajos/$',views.listado_trabajos, name='listado'),
    url(r'^listado-trabajos/detalles/(?P<id_trabajo>\d+)$',views.detalles_resumen, name='detalles_resumen'),
    url(r'^$', views.arbitrajes_pag, name= 'arbitrajes'),
    url(r'^asignar-sesion/$',views.asignacion_de_sesion, name='asignacion_de_sesion'),
    url(r'^arbitro/listar-arbitros/$',views.referee_list,name='referee_list'),
    url(r'^arbitro/editar-arbitro/$',views.referee_edit,name='referee_edit'),
    # url(r'^areas-subareas/$',views.areas_subareas,name='arbitrations_areas_subareas'),

    #Carga de contenido 
    url(r'^listArbitros$',views.list_arbitros,name='list_arbitros'),
    
    # CRUD Arbitros
    url(r'^arbitro/listar-arbitros/viewArbitro/(?P<id>\d+)$',views.viewArbitro,name='verArbitro'),
    url(r'^arbitro/listar-arbitros/editArbitro/(?P<id>\d+)$',views.editArbitro,name='editarArbitro'),
    url(r'^arbitro/listar-arbitros/removeArbitro/(?P<id>\d+)$',views.removeArbitro,name='eliminarArbitro'),

    # Generar Reportes
    url(r'^generar_reporte/(?P<tipo>\d+)$',views.generate_report,name='generar_reporte'),
    
]