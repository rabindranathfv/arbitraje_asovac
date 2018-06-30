# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from arbitrajes.models import Arbitraje, Area, Sub_area, Arbitro
# Register your models here.

admin.site.register(Arbitraje)
admin.site.register(Area)
admin.site.register(Sub_area)
admin.site.register(Arbitro)