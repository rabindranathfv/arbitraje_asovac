# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from trabajos.models import Trabajo,Trabajo_arbitro
# Register your models here.

admin.site.register(Trabajo)
# admin.site.register(Detalle_version_final)
admin.site.register(Trabajo_arbitro)