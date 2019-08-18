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
from django.contrib.auth.views import logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from main_app.views import login_view
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ## add routing using include in apps / The namespace allows for url tag convention to be used in templates.
    url(r'^administracion/', include('main_app.urls', namespace='main_app')),
    url(r'^arbitrajes/', include('arbitrajes.urls', namespace='arbitrajes')),
    url(r'^recursos/', include('recursos.urls', namespace='recursos')),
    url(r'^seguimiento/', include('seguimiento.urls', namespace='seguimiento')),
    url(r'^sesiones/', include('sesiones.urls', namespace='sesiones')),
    url(r'^trabajos/', include('trabajos.urls', namespace='trabajos')),
    url(r'^eventos/', include('eventos.urls', namespace='eventos')),
    url(r'^autores/', include('autores.urls', namespace='autores')),

     ## password and login 

    url(r'^logout/', logout_then_login, name='logout'),
    url(r'^$',login_view, name = 'login'),

    #url(r'^accounts/login/',login,{'template_name':'main_app_login.html'},name='login'),
    
    url(r'^reset/password_reset$', password_reset, 
        {'template_name':'password_reset_form.html',
        'email_template_name': 'email_templates/password_reset_email_txt.html',
        'html_email_template_name': 'email_templates/password_reset_email.html',
        'subject_template_name': 'email_templates/password_reset_subject.txt'},
        name='password_reset'),
    url(r'^password_reset_done$', password_reset_done, 
        {'template_name': 'password_reset_done.html'}, 
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, 
        {'template_name': 'password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done$', password_reset_complete, {'template_name': 'password_reset_complete.html'},
        name='password_reset_complete'),
    
]

# add config for link styles, for collectstatic
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)