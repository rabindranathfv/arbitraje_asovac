# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def configuration_guard(estado, rol_id):
    if not ( (estado == 0 and 2 == rol_id) or ((estado != 1 and estado != 8) and 3 == rol_id) or ((estado != 8) and 4 == rol_id) or 5 == rol_id):
        return True
    else:
        return False

def configuration_general_guard(estado, rol_id):
    if 1 >= rol_id or (estado != 0 and 2 >= rol_id):
        return True
    else:
        return False

def datos_basicos_guard(estado, rol_id):
    if not (estado == 2 and (1 != rol_id and 2 != rol_id)) or (estado == 4 and (1 != rol_id and 2 != rol_id)):
        return True
    else:
        return False

def usuarios_guard(rol_id):
    if rol_id == 1:
        return True
    else:
        return False

def areas_subareas_guard(estado, rol_id):
    if (1 >= rol_id) or (estado == 1 and (2 >= rol_id or 3 >= rol_id)) or (estado == 2 and 2 >= rol_id):
        return True
    else:
        return False