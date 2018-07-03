# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from sesiones.models import Espacio_fisico, Espacio_virtual, Espacio, Sesion 
# Register your models here.

admin.site.register(Espacio)
admin.site.register(Espacio_virtual)
admin.site.register(Espacio_fisico)
admin.site.register(Sesion)
