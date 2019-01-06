# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from arbitrajes.models import Arbitraje, Arbitro #,Arbitros_Sistema_asovac
# Register your models here.

admin.site.register(Arbitraje)
admin.site.register(Arbitro)
# admin.site.register(Arbitros_Sistema_asovac)