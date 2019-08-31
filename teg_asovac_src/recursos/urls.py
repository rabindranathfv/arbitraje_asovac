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
    url(r'^$', views.recursos_pag, name='recursos'),
    url(r'^pdf/$', views.create_authors_certificates, name='generate_pdf'),#generate_pdf  #create_authors_certificates
    url(r'^certificado/autor-certificado/$', views.resources_author, name='resources_author'),
    url(r'^certificado/arbitro-certificado/$', views.resources_referee, name='resources_referee'),
    url(r'^certificado/organizador-certificado/$', views.resources_organizer, name='resources_organizer'),
    url(r'^certificado/conferencista-certificado/$', views.resources_lecturer, name='resources_lecturer'),

    url(r'^conferencista-importar-excel/$',views.load_lecturers_modal,name='load_lecturers_modal'),
    url(r'^organizador-importar-excel/$',views.load_organizers_modal,name='load_organizers_modal'),

    url(r'^documentos/eventos/$', views.resources_event, name='resources_event'),
    url(r'^documentos/eventos/comision-logistica$',
        views.create_logistics_certificates, name='create_logistics_certificates'),
    url(r'^certificado/arbitraje-certificado/$',
        views.resources_arbitration, name='resources_arbitration'),
    url(r'^documentos/sesion/$', views.resources_sesion, name='resources_sesion'),
    url(r'^documentos/sesion/coordinador-sesion/$',
        views.create_session_coord_certificates, name='create_session_coord_certificates'),
    url(r'^certificado/trabajo-certificado/$', views.resources_paper, name='resources_paper'),
    url(r'^documentos/asovac/$', views.resources_asovac, name='resources_asovac'),
    url(r'^documentos/asovac/comision-organizadora$',
        views.create_organizer_comitee_certificates, name='create_organizer_comitee_certificates'),

    url(r'^api/data/$', views.get_data, name='get_data'),
    url(r'^api/chart/data/$', views.ChartData.as_view(), name='chart_data'),


    url(r'^format-participants/(?P<option>\d+)/$', views.format_import_participants, name='format_import_participants'),
]
