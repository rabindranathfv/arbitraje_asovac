# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def recursos_guard(estado, rol_id):
    if (rol_id in [1,2]) or (estado >= 7 and (3 >= rol_id  or 4 >= rol_id)):
        return True
    else:
        return False

def resultados_guard(estado, rol_id):
    if not ( ((estado !=6 and estado != 7 and estado != 8) and 2 == rol_id) or ((estado != 6 and estado != 8) and 3 == rol_id) or ((estado != 8 and estado != 6) and 4 == rol_id) or (estado != 6 and 5 == rol_id)):
        return True
    else:
        return False