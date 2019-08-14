# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Usuario_rol_in_sistema, Rol, Sistema_asovac, Usuario_asovac


class DashboardCharts(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        arbitraje_id = request.session['arbitraje_id']
        #El siguiente codigo es para obtener los datos necesarios para la grafica de usuarios
        #distribuidos por roles
        coord_area_count = Usuario_rol_in_sistema.objects.filter(rol=3,
                                                                 sistema_asovac=arbitraje_id,
                                                                 status=True).count()
        referee_count = Usuario_rol_in_sistema.objects.filter(rol=4,
                                                              sistema_asovac=arbitraje_id,
                                                              status=True).count()
        author_count = Usuario_rol_in_sistema.objects.filter(rol=5,
                                                             sistema_asovac=arbitraje_id,
                                                             status=True).count()
        #El siguiente codigo es para obtener los datos necesarios para la grafica de genero
        #de los autores
        women_count = Usuario_rol_in_sistema.objects.filter(rol=5,
                                                            usuario_asovac__autor__genero=1,
                                                            sistema_asovac=arbitraje_id,
                                                            status=True).count()
        men_count = Usuario_rol_in_sistema.objects.filter(rol=5,
                                                          usuario_asovac__autor__genero=0,
                                                          sistema_asovac=arbitraje_id,
                                                          status=True).count()

        data = {
            "usuarios": {
                "labels": ["Coordinadores de Área", "Árbitros", "Autores"],
                "data": [coord_area_count, referee_count, author_count]
            },
            "generos": {
                "labels": ["Mujeres", "Hombres"],
                "data": [women_count, men_count]
            },
            # "arbitros": {
            #     "labels": ['Total árbitros', 'Invitaciones aceptadas', 'Invitaciones pendientes'],
            #     "data": [total_arbitros, invitaciones_aceptadas, invitaciones_pendientes]
            # },
            # "autores": {
            #     "labels": ['Educación Básica Primaria', 'Educación Básica Secundaria', 'Bachillerato/Educación Media', 'Educación Técnico/Profesional', 'Universidad', 'Postgrado'],
            #     "data": [educacion_primaria, educacion_secundaria, bachillerato, tecnico, universidad, postgrado]
            # },
            # "area":{
            #     "labels": areas_labels_splited,
            #     "data_aceptados": areas_trabajos_aceptados,
            #     "data_rechazados": areas_trabajos_rechazados,
            # },
            # "autoresArea":{
            #     "labels": areas_labels,
            #     "data": areas_autores,
            #     "colores": areas_colores
            # },
        }
        return Response(data)
