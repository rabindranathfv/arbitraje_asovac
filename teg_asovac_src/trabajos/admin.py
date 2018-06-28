# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from trabajos.models import Trabajo, Detalle_version_final
# Register your models here.

admin.site.register(Trabajo)
admin.site.register(Detalle_version_final)