# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def referee_guard(estado, rol_id):
    if (1 >= rol_id) or (estado == 1 and 2 >= rol_id) or ((estado ==2 or estado == 3 or estado == 4) and (2 >= rol_id or 3 >= rol_id)) or (estado ==1 and 3 >= rol_id):
        return True
    else:
        return False