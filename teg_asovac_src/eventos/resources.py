from import_export import resources
from .models import Organizador, Locacion_evento, Evento, Organizador_evento

class OrganizadorResource(resources.ModelResource):
    class Meta:
        model = Organizador

class LocacionResource(resources.ModelResource):
    class Meta:
        model = Locacion_evento

class EventoResource(resources.ModelResource):
    class Meta:
        model = Evento
        # Se excluye la relacion m2m para ser importada en su propia funcionalidad.
        exclude = ('organizador_id', )

class OrganizadoresEventosResource(resources.ModelResource):
    class Meta:
        model = Organizador_evento