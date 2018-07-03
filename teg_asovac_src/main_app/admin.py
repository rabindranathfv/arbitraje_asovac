# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from main_app.models import Rol, Usuario_asovac, Sistema_asovac
# Register your models here.

admin.site.register(Rol)
admin.site.register(Usuario_asovac)
admin.site.register(Sistema_asovac)