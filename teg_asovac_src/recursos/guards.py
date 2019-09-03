
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def recursos_guard(estado, rol_id):
    if (rol_id in [1,2]) or (estado >= 7 and (3 >= rol_id  or 4 >= rol_id)):
        return True
    else:
        return False