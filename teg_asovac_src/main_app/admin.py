# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from main_app.models import Rol, Usuario_asovac, Sistema_asovac, Area, Sub_area, Usuario_rol_in_sistema
# Register your models here.

admin.site.register(Rol)
admin.site.register(Usuario_asovac)
admin.site.register(Sistema_asovac)
admin.site.register(Area)
admin.site.register(Sub_area)
admin.site.register(Usuario_rol_in_sistema)