# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('usuario.views',
    url(r'^usuario/$','usuario', name='ogcs-mantenimiento-usuario'),
)
