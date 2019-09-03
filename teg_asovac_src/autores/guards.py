# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def autores_guard(estado, rol_id):
    if (1 >= rol_id) or ((estado == 1 or estado ==2 or estado == 3 or estado == 4) and (2 >= rol_id)):
        return True
    else:
        return False