from django.core.exceptions import PermissionDenied
from .models import  Usuario_rol_in_sistema,Usuario_asovac,User,Rol
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse

def user_is_arbitraje(function):
    def wrap(request, *args, **kwargs):

        user = get_object_or_404(User, id = request.user.id)
        usuario_asovac = get_object_or_404(Usuario_asovac, usuario = user)
        rol = Rol.objects.get(id = 1)
        # arbitraje = Sistema_asovac.objects.get(id = request.session['arbitraje_id'])
        is_admin= Usuario_rol_in_sistema.objects.filter(rol= rol, usuario_asovac = usuario_asovac).exists()

        if is_admin == True:
            if 'arbitraje_id' in request.session and 'estado' in request.session:
                return function(request, *args, **kwargs)
            else:
                return redirect('main_app:home')
        else:
            if 'arbitraje_id' in request.session and 'estado' in request.session:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
                
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap