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
    url(r'^$', views.home, name= 'home'),
    url(r'^listar-eventos/$',views.event_list,name='event_list'),
    url(r'^exportar-eventos/$',views.event_export_excel,name='event_export_excel'),
    url(r'^importar-eventos/$',views.event_import_excel,name='event_import_excel'),
    url(r'^exportar-organizadores-de-eventos/$',views.organizers_events_export_excel,name='organizers_events_export_excel'),
    url(r'^importar-organizadores-de-eventos/$',views.organizers_events_import_excel,name='organizers_events_import_excel'),
    url(r'^editar-evento/(?P<evento_id>\d+)/$',views.event_edit,name='event_edit'),
    url(r'^crear-evento/$',views.event_create,name='event_create'),
    url(r'^detalles-evento/(?P<evento_id>\d+)/$',views.event_detail,name='event_detail'),
    url(r'^eliminar-evento/(?P<evento_id>\d+)/$',views.event_delete,name='event_delete'),

    url(r'^crear-organizador/$',views.organizer_create,name='organizer_create'),
    url(r'^listar-organizadores/$',views.organizer_list,name='organizer_list'),
    url(r'^exportar-organizadores/$',views.organizer_export_excel,name='organizer_export_excel'),
    url(r'^importar-organizadores/$',views.organizer_import_excel,name='organizer_import_excel'),
    url(r'^editar-organizador/(?P<organizador_id>\d+)/$',views.organizer_edit,name='organizer_edit'),
    url(r'^eliminar-organizador/(?P<organizador_id>\d+)/$',views.organizer_delete,name='organizer_delete'),
    url(r'^detalles-organizador/(?P<organizador_id>\d+)/$',views.organizer_detail,name='organizer_detail'),

    url(r'^crear-locacion/$',views.event_place_create,name='event_place_create'),
    url(r'^listar-locaciones/$',views.event_place_list,name='event_place_list'),
    url(r'^exportar-locaciones/$',views.event_place_export_excel,name='event_place_export_excel'),
    url(r'^importar-locaciones/$',views.event_place_import_excel,name='event_place_import_excel'),
    url(r'^editar-locacion/(?P<locacion_id>\d+)/$',views.event_place_edit,name='event_place_edit'),
    url(r'^eliminar-locacion/(?P<locacion_id>\d+)/$',views.event_place_delete,name='event_place_delete'),
    url(r'^detalles-locacion/(?P<locacion_id>\d+)/$',views.event_place_detail,name='event_place_detail'),

    url(r'^agregar-organizador/(?P<evento_id>\d+)/$',views.add_organizer_to_event, name='add_organizer_to_event'),
    url(r'^agregar-observaciones/(?P<evento_id>\d+)/$',views.add_observations_to_event, name='add_observations_to_event'),
    url(r'^locacion/agregar-observaciones/(?P<locacion_id>\d+)/$',views.add_observations_to_event_place, name='add_observations_to_event_place'),
    url(r'^organizador/agregar-observaciones/(?P<organizador_id>\d+)/$',views.add_observations_to_organizer, name='add_observations_to_organizer'),
]