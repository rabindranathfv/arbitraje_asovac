from import_export import fields, resources
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from django.contrib.auth.models import User
from .models import Usuario_asovac, Rol, Sistema_asovac

class UserResource(resources.ModelResource):
    #usuario = fields.Field(column_name='usuario', attribute='User', widget=ForeignKeyWidget(User, 'pk'))
    #rol = fields.Field(widget=ManyToManyWidget(Rol))
    #Sistema_asovac_id = fields.Field(widget=ManyToManyWidget(Sistema_asovac))

    class Meta:
        model = User
        #fields = ('usuario', 'rol', 'Sistema_asovac_id','estado_arbitraje', 'usuario_activo')

class UsuarioAsovacResource(resources.ModelResource):
    #usuario = fields.Field(column_name='usuario', attribute='User', widget=ForeignKeyWidget(User, 'pk'))
    #rol = fields.Field(widget=ManyToManyWidget(Rol))
    #Sistema_asovac_id = fields.Field(widget=ManyToManyWidget(Sistema_asovac))

    class Meta:
        model = Usuario_asovac
        #fields = ('usuario', 'rol', 'Sistema_asovac_id','estado_arbitraje', 'usuario_activo')

class SistemaAsovacResource(resources.ModelResource):
    #usuario = fields.Field(column_name='usuario', attribute='User', widget=ForeignKeyWidget(User, 'pk'))
    #rol = fields.Field(widget=ManyToManyWidget(Rol))
    #Sistema_asovac_id = fields.Field(widget=ManyToManyWidget(Sistema_asovac))

    class Meta:
        model = Sistema_asovac