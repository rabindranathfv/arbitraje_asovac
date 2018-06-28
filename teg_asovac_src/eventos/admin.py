# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from eventos.models import Organizador, Locacion_evento, Evento, Organizador_evento
# Register your models here.

admin.site.register(Organizador)
admin.site.register(Locacion_evento)
admin.site.register(Evento)
admin.site.register(Organizador_evento)
