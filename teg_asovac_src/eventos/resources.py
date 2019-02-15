from import_export import resources
from .models import Organizador, Locacion_evento

class OrganizadorResource(resources.ModelResource):
    class Meta:
        model = Organizador

class LocacionResource(resources.ModelResource):
    class Meta:
        model = Locacion_evento