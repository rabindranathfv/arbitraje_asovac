# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def trabajos_seguimiento_guard(estado, rol_id):
    if (((estado ==3 or estado ==4 or estado ==5) and (2 >= rol_id or 3 >= rol_id)) or (1 >= rol_id) or (estado ==6 and 3 >= rol_id)) and not ( ((estado == 0 or estado == 8) and 2 == rol_id) or ((estado == 0 or estado == 8) and 3 == rol_id) or 4 == rol_id or 5 == rol_id):
        return True
    else:
        return False


def trabajos_guard(estado, rol_id):
    if((estado == 3 or estado == 5 or estado == 8 ) and 5 >= rol_id):
        return True
    else:
        return False

def add_new_job_version_guard(estado, rol_id):
    if(estado == 5 and 5 >= rol_id):
        return True
    else:
        return False