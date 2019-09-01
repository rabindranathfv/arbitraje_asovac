"""core_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.shortcuts import render
#import settings
from django.conf import settings
# import para envio de correo
from django.core.mail import send_mail
#import for use include
from django.conf.urls import include
#import para collect static y usar media
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, password_reset_confirm, password_reset_complete


from . import views
from . import utils as utilsViews

urlpatterns = [
    # url(r'^$',views.login,name='login'),
    url(r'^home/$',views.home,name='home'),
    url(r'^(?P<arbitraje_id>\d+)/$',views.dashboard,name='dashboard'),
    url(r'^crear-arbitraje/$',views.create_arbitraje, name='create_arbitraje'),
    url(r'^(?P<arbitraje_id>\d+)/datos-basicos/$',views.data_basic,name='data_basic'),
    url(r'^(?P<arbitraje_id>\d+)/crear-clave-COG/$',views.generate_COG_key,name='generate_COG_key'),
    url(r'^(?P<arbitraje_id>\d+)/crear-clave-COA/$',views.generate_COA_key,name='generate_COA_key'),
    url(r'^(?P<arbitraje_id>\d+)/crear-clave-ARS/$',views.generate_ARS_key,name='generate_ARS_key'),
    url(r'^(?P<arbitraje_id>\d+)/estado-arbitraje/$',views.state_arbitration,name='arbitration_state'),
    url(r'^(?P<arbitraje_id>\d+)/usuarios/listar-usuarios/$',views.users_list,name='users_list'),
    url(r'^(?P<arbitraje_id>\d+)/usuarios/editar-usuario/$',views.user_edit,name='user_edit'),
    url(r'^(?P<arbitraje_id>\d+)/usuarios/roles/$',views.user_roles,name='user_roles'),
    url(r'^(?P<arbitraje_id>\d+)/coordinador-general/$',views.coord_general,name='coord_general'),
    url(r'^(?P<arbitraje_id>\d+)/coordinador-area/$',views.coord_area,name='coord_area'),
    url(r'^(?P<arbitraje_id>\d+)/resultados-total/$',views.total,name='total'),
    url(r'^registrar/$',views.register, name='register'), 
    url(r'^email-test/$',views.email_test, name='email_test'),
    #url(r'^', include('eventos.urls')),
    url(r'^aplicaciones/$',views.apps_selection,name='apps_selection'),
    url(r'^areas-subareas/$',views.areas_subareas,name='arbitrations_areas_subareas'),
    # Carga de tablas via archivos
    url(r'^load/areas$',views.load_areas_modal,name='load_areas'),
    url(r'^load/subareas$',views.load_subareas_modal,name='load_subareas'),
    url(r'^(?P<arbitraje_id>\d+)/load/(?P<rol>\d+)/usuarios$',views.load_users_modal,name='load_users'),
    
    # Agrega usuarios al evento
    url(r'^(?P<arbitraje_id>\d+)/load/arbitraje$',views.load_users_arbitraje_modal,name='load_users_arbitraje'),

    #Carga de contenido 
    url(r'^list$',views.list,name='list'),
    url(r'^listSubareas$',views.list_subareas,name='list_subareas'),
    url(r'^listUsuarios$',views.list_usuarios,name='list_usuarios'),
    
    # CRUD Areas
    url(r'^areas-subareas/viewArea/(?P<id>\d+)$',views.viewArea,name='verArea'),
    url(r'^areas-subareas/editArea/(?P<id>\d+)$',views.editArea,name='editarArea'),
    url(r'^areas-subareas/removeArea/(?P<id>\d+)$',views.removeArea,name='eliminarArea'),
    
    # CRUD Subareas
    url(r'^areas-subareas/viewSubarea/(?P<id>\d+)$',views.viewSubarea,name='verSubarea'),
    url(r'^areas-subareas/editSubarea/(?P<id>\d+)$',views.editSubarea,name='editarSubarea'),
    url(r'^areas-subareas/removeSubarea/(?P<id>\d+)$',views.removeSubarea,name='eliminarSubarea'),

    # CRUD Usuarios
    url(r'^(?P<arbitraje_id>\d+)/usuarios/listar-usuarios/viewUsuario/(?P<id>\d+)$',views.viewUsuario,name='verUsuario'),
    url(r'^(?P<arbitraje_id>\d+)/usuarios/listar-usuarios/editUsuario/(?P<id>\d+)$',views.editUsuario,name='editarUsuario'),
    url(r'^(?P<arbitraje_id>\d+)/usuarios/listar-usuarios/removeUsuario/(?P<id>\d+)$',views.removeUsuario,name='eliminarUsuario'),
    url(r'^(?P<arbitraje_id>\d+)/usuarios/listar-usuarios/changeRol/(?P<id>\d+)$',views.changeRol,name='cambiarRol'),
    
    #Rutas para modales ajax
    url(r'^usuario/crear$',views.create_user_modal,name='crear_usuario'),
    url(r'^usuario/cambiar-clave/$',views.changepassword_modal,name='changepassword_modal'),
    url(r'^usuario/(?P<id>\d+)/actualizar$',views.update_user_modal,name='actualizar_usuario'),
    url(r'^usuario/(?P<id>\d+)/eliminar$',views.delete_user_modal,name='eliminar_usuario'),
    url(r'^usuario/(?P<id>\d+)/rol/actualizar$',views.update_rol_modal,name='actualizar_rol'),
    url(r'^usuario/(?P<id>\d+)/rol/validar$',views.validate_access_modal,name='validar_rol'),
    url(r'^usuario/(?P<user_id>\d+)/crear-autor/$',views.create_autor_instance_modal,name='create_autor_instance_modal'),
    url(r'^usuario/(?P<arbitraje_id>\d+)/registrar-en-sistema/$',views.register_user_in_sistema,name='register_user_in_sistema'),
    url(r'^usuario/editar$',views.edit_personal_data,name='edit_personal_data'),

    url(r'^cargar/(?P<id>\d+)/subarea$',views.get_subareas,name='cargar_subareas'),
    url(r'^validar/acceso$',views.validate_access_modal,name='validar_acceso'),

    # Generar Reportes
    url(r'^generar_reporte/(?P<tipo>\d+)$',views.generate_report,name='generar_reporte'),

    # API de Graficos de Dashboard
    url(r'^dashboard/chart/data/$',
        utilsViews.DashboardCharts.as_view(), name='dashboard_chart_data'),
]