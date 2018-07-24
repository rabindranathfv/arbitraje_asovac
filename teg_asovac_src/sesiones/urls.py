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
    url(r'^dashboard/admin/sesions/list/$', views.sesions_list, name= 'sesions_list'),
    url(r'^dashboard/admin/sesions/edit/$', views.sesions_edit, name= 'sesions_edit'),
    url(r'^dashboard/admin/sesions/space/list/$', views.sesions_space_list, name= 'sesions_space_list'),
    url(r'^dashboard/admin/sesions/space/edit/$', views.sesions_space_edit, name= 'sesions_space_edit'),
]