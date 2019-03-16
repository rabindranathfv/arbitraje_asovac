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

    # CRUD Trabajos
    url(r'^listar-trabajos/selectArbitro/(?P<id>\d+)$',views.selectArbitro,name='selectArbitro'),
    url(r'^listar-trabajos/viewTrabajo/(?P<id>\d+)$',views.viewTrabajo,name='verTrabajo'),

    # Generar Reportes
    url(r'^generar_reporte/(?P<tipo>\d+)$',views.generate_report,name='generar_reporte'),

    # Ajax
    url(r'^eliminar/(?P<trabajo_id>\d+)/$',views.delete_job , name='delete_job'),
    url(r'^resultados/observaciones/(?P<trabajo_version_final_id>\d+)/$',views.show_job_observations , name='show_job_observations'),
    url(r'^resultados/observaciones/agregar/(?P<trabajo_version_final_id>\d+)/$',views.autor_add_observations_to_job , name='autor_add_observations_to_job'),
    url(r'^mostrar/(?P<id>\d+)/areas$',views.show_areas_modal,name='mostrar_areas'),
    url(r'^agregar-autor/(?P<autor_trabajo_id>\d+)/$',views.add_author_to_job , name='add_author_to_job'),
    url(r'^crear-nueva-version/(?P<last_version_trabajo_id>\d+)/$',views.add_new_version_to_job , name='add_new_version_to_job'),
]
