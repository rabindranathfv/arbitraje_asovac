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
    url(r'^pdf/$', views.generate_pdf, name= 'generate_pdf'),
    url(r'^administracion/autor/$',views.resources_author,name='resources_author'),
    url(r'^administracion/arbitro/$',views.resources_referee,name='resources_referee'),
    url(r'^administracion/evento/$',views.resources_event,name='resources_event'),
    url(r'^administracion/arbitraje/$',views.resources_arbitration,name='resources_arbitration'),
    url(r'^administracion/sesion/$',views.resources_sesion,name='resources_sesion'),
    url(r'^administracion/asovac/$',views.resources_asovac,name='resources_asovac'),
]