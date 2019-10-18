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
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^trabajos-por-arbitrar/$', views.jobs_for_review, name='jobs_for_review'),
    url(r'^listado-trabajos/detalles/(?P<id_trabajo>\d+)$',
        views.detalles_resumen, name='detalles_resumen'),
    url(r'^estatus-trabajos/$', views.estatus_trabajos, name='listado'),
    url(r'^listado-trabajos/detalles/$', views.detalles_resumen, name='detalles_resumen'),
    url(r'^$', views.arbitrajes_pag, name='arbitrajes'),
    url(r'^asignar-sesion/$', views.asignacion_de_sesion, name='asignacion_de_sesion'),
    url(r'^arbitro/listar-arbitros/$', views.referee_list, name='referee_list'),
    url(r'^arbitro/editar-arbitro/$', views.referee_edit, name='referee_edit'),
    url(r'^arbitrar-trabajo/(?P<trabajo_id>\d+)$', views.review_job, name='review_job'),
    # url(r'^areas-subareas/$',views.areas_subareas,name='arbitrations_areas_subareas'),

    #Carga de contenido
    url(r'^listArbitros$', views.list_arbitros, name='list_arbitros'),
    url(r'^listArbitrajes$', views.list_arbitrajes, name='list_arbitrajes'),
    url(r'^listTrabajosAceptados$', views.list_trabajos_aceptados, name='list_trabajos_aceptados'),
    url(r'^listAreasArbitros/(?P<id>\d+)$', views.list_areas_arbitros, name='list_areas_arbitros'),
    url(r'^listSubAreasArbitros/(?P<id>\d+)$',views.list_subareas_arbitros, name='list_subareas_arbitros'),
    url(r'^listAreasUsuarios/(?P<id>\d+)$', views.list_areas_usuarios, name='list_areas_usuarios'),
    url(r'^listSubAreasUsuarios/(?P<id>\d+)$',views.list_subareas_usuarios, name='list_subareas_usuarios'),
    url(r'^getSubareas/(?P<id>\d+)$', views.getSubareas, name='getSubareas'),

    # CRUD Arbitros
    url(r'^arbitro/listar-arbitros/viewArbitro/(?P<id>\d+)$', views.viewArbitro, name='verArbitro'),
    url(r'^arbitro/listar-arbitros/editArbitro/(?P<id>\d+)$',
        views.editArbitro, name='editarArbitro'),
    url(r'^arbitro/listar-arbitros/removeArbitro/(?P<id>\d+)$',
        views.removeArbitro, name='eliminarArbitro'),
    url(r'^arbitro/listar-arbitros/adminArea/(?P<id>\d+)$', views.adminArea, name='adminArea'),
    url(r'^arbitro/listar-arbitros/adminArea/(?P<id>\d+)/removeSubareaArbitro/(?P<subarea>\d+)$',
        views.adminRemoveSubarea, name='adminRemoveSubarea'),
    url(r'^arbitro/listar-arbitros/adminArea/(?P<id>\d+)/addSubareaArbitros$',
        views.adminAddSubareas, name='adminAddSubareas'),
    url(r'^arbitro/listar-arbitros/adminArea/(?P<id>\d+)/addareaArbitros$',
        views.adminAddareas, name='adminAddAreas'),
    url(r'^arbitro/listar-arbitros/adminArea/(?P<id>\d+)/changeAreaArbitro$',
        views.adminChangeAreas, name='adminChangeAreas'),

    # CRUD Arbitraje
    url(r'^estatus-trabajos/viewArbitraje/(?P<id>\d+)$', views.viewArbitraje, name='verArbitraje'),
    url(r'^estatus-trabajos/changeStatus/(?P<id>\d+)$', views.changeStatus, name='cambiarEstatus'),
    url(r'^estatus-trabajos/statusArbitraje/(?P<id>\d+)$',
        views.statusArbitraje, name='estatusArbitraje'),
    url(r'^estatus-trabajos/newArbitraje/(?P<id>\d+)$', views.newArbitraje, name='nuevoArbitraje'),

    # CRUD Trabajos Aceptados
    url(r'^asignar-sesion/editPresentacion/(?P<id>\d+)$',
        views.editPresentacion, name='editarPresentacion'),
    url(r'^asignar-sesion/asignarSesion/(?P<id>\d+)$', views.asigSesion, name='asignarSesion'),

    # Generar Reportes
    url(r'^generar_reporte/(?P<tipo>\d+)$', views.generate_report, name='generar_reporte'),
]
