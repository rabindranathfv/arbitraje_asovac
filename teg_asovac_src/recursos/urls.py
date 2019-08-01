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
    url(r'^$', views.recursos_pag, name= 'recursos'),
    url(r'^pdf/$', views.create_authors_certificates, name= 'generate_pdf'),#generate_pdf
    url(r'^certificado/autor-certificado/$',views.resources_author,name='resources_author'),
    url(r'^certificado/arbitro-certificado/$',views.resources_referee,name='resources_referee'),
    url(r'^certificado/evento-certificado/$',views.resources_event,name='resources_event'),
    url(r'^certificado/arbitraje-certificado/$',views.resources_arbitration,name='resources_arbitration'),
    url(r'^certificado/sesion-certificado/$',views.resources_sesion,name='resources_sesion'),
    url(r'^certificado/asovac-certificado/$',views.resources_asovac,name='resources_asovac'),

    #Ajax
    url(r'^api/data/$', views.get_data, name= 'get_data'),
    url(r'^api/chart/data/$', views.ChartData.as_view(), name = 'chart_data'),

]