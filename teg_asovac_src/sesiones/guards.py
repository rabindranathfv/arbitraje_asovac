# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def sesiones_seguimiento_guard(estado, rol_id):
    if ((1 >= rol_id ) or (estado == 4 and (2 >= rol_id or 3 >= rol_id)) or (estado ==7 and 2 >= rol_id)) and not (((estado == 0 or estado == 8) and 2 == rol_id) or ((estado == 0 or estado == 8) and 3 == rol_id) or 4 == rol_id or 5 == rol_id):
        return True
    else:
        return False