from import_export import resources
from .models import Organizador, Locacion_evento, Evento

class OrganizadorResource(resources.ModelResource):
    class Meta:
        model = Organizador

class LocacionResource(resources.ModelResource):
    class Meta:
        model = Locacion_evento

class EventoResource(resources.ModelResource):
    class Meta:
        model = Evento
        exclude = ('organizador_id', )