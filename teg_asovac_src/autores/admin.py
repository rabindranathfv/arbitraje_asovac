# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from autores.models import Universidad, Autor, Autores_trabajos, Datos_pagador, Pagador, Pago, Factura
# Register your models here.


admin.site.register(Universidad)
admin.site.register(Autor)
admin.site.register(Autores_trabajos)
admin.site.register(Datos_pagador)
admin.site.register(Pago)
admin.site.register(Pagador)
admin.site.register(Factura)
