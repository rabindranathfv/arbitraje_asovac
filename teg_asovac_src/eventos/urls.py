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
    #url(r'^$', views.eventos_pag, name= 'eventos'),
    url(r'^lista-eventos/$',views.event_list,name='event_list'),
    url(r'^editar-evento/$',views.event_edit,name='event_edit'),
    url(r'^crear-evento/$',views.event_create,name='event_create'),

    url(r'^crear-organizador/$',views.organizer_create,name='organizer_create'),
    url(r'^listar-organizadores/$',views.organizer_list,name='organizer_list'),
    url(r'^editar-organizador/$',views.organizer_edit,name='organizer_edit'),
    url(r'^eliminar-organizador/$',views.organizer_delete,name='organizer_delete'),
    url(r'^detalles-organizador/$',views.organizer_detail,name='organizer_detail'),
]