from django.conf import settings
from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        route= dict()
        if 'next' in request.GET:
            # print request.GET['next']
            route= {'next':"/administracion/home/"}
            request.GET = route
        
        if not request.user.is_authenticated() :
            # return redirect(reverse('login'))
          #Can't log out if not logged in
            return

        try:
            # print "Restante {}".format(datetime.now() - request.session['last_touch'] )
            # print "limite {}".format(timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0))
            # print datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0)
            if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                auth.logout(request)
                return redirect(reverse('logout'))
                del request.session['last_touch']
                return
        except KeyError:
            pass

        request.session['last_touch'] = datetime.now()