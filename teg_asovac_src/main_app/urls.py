"""core_app URL Configuration

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
from django.contrib import admin

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
#import for use include
from django.conf.urls import include
#import para collect static y usar media
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete


from . import views
from main_app.views import register

urlpatterns = [
    # url(r'^$',views.login,name='login'),
    url(r'^home/$',views.home,name='home'),
    url(r'^dashboard/$',views.dashboard,name='dasboard'),
    url(r'^crear-arbitraje/$',views.create_arbitraje, name='create_arbitraje'),
    url(r'^dashboard/admin/data_basic$',views.data_basic,name='data_basic'),
    url(r'^dashboard/admin/arbitration/state$',views.state_arbitration,name='arbitration_state'),
    url(r'^dashboard/admin/users/list$',views.users_list,name='users_list'),
    url(r'^dashboard/admin/user/edit$',views.user_edit,name='user_edit'),
    url(r'^dashboard/admin/user/roles$',views.user_roles,name='user_roles'),
    url(r'^dashboard/admin/coord/general$',views.coord_general,name='coord_general'),
    url(r'^dashboard/admin/coord/area$',views.coord_area,name='coord_area'),
    url(r'^dashboard/admin/total$',views.total,name='total'),
    url(r'^crear-arbitraje/$',views.create_arbitraje, name='create_arbitraje'), 
    url(r'^register/$',views.register, name='register'), 
    #url(r'^', include('eventos.urls')),
]