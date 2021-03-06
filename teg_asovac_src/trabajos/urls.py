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

    #Carga de contenido 
    url(r'^listTrabajos$',views.list_trabajos,name='list_trabajos'),
    url(r'^listPagos/(?P<id>\d+)$',views.list_pagos,name='list_pagos'),

    # CRUD Trabajos
    url(r'^listar-trabajos/selectArbitro/(?P<id>\d+)$',views.selectArbitro,name='selectArbitro'),
    url(r'^listar-trabajos/checkPago/(?P<id>\d+)$',views.checkPago,name='checkPago'),
    url(r'^listar-trabajos/viewTrabajo/(?P<id>\d+)$',views.viewTrabajo,name='verTrabajo'),
    url(r'^listar-trabajos/statusArbitro/(?P<id>\d+)$',views.viewEstatus,name='verEstatus'),
    url(r'^invitacion/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.invitacion, name='invitacion'),
    url(r'^listar-trabajos/validatePago/(?P<id>\d+)/$',views.validatePago,name='validatePago'),
    url(r'^listar-trabajos/solicitad-nuevo-pago/(?P<trabajo_id>\d+)/$',views.request_new_pay,name='request_new_pay'),
    url(r'^listar-trabajos/review_pay/(?P<factura_id>\d+)/$',views.review_pay,name='review_pay'),

    # Generar Reportes
    url(r'^generar_reporte/(?P<tipo>\d+)$',views.generate_report,name='generar_reporte'),

    # Ajax
    url(r'^eliminar/(?P<trabajo_id>\d+)/$',views.delete_job , name='delete_job'),
    url(r'^resultados/observaciones/(?P<trabajo_version_final_id>\d+)/$',views.show_job_observations , name='show_job_observations'),
    # url(r'^resultados/observaciones/agregar/(?P<trabajo_version_final_id>\d+)/$',views.autor_add_observations_to_job , name='autor_add_observations_to_job'),
    url(r'^mostrar/(?P<id>\d+)/areas$',views.show_areas_modal,name='mostrar_areas'),
    url(r'^agregar-autor/(?P<autor_trabajo_id>\d+)/$',views.add_author_to_job , name='add_author_to_job'),
    url(r'^crear-nueva-version/(?P<last_version_trabajo_id>\d+)/$',views.add_new_version_to_job , name='add_new_version_to_job'),
    url(r'^resultados/arbitraje/(?P<trabajo_id>\d+)/$',views.view_referee_observation , name='view_referee_observation'),    
        
]
