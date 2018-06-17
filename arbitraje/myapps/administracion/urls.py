from django.conf.urls import url

from myapps.administracion.views import index_admin

urlpatterns = [
    url(r'^$', index_admin),
]