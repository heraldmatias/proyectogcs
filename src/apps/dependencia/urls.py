# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('dependencia.views',
    url(r'^ministerio/$','ministerio', name='ogcs-mantenimiento-ministerio'),
    url(r'^odp/$','odp', name='ogcs-mantenimiento-odp'),    
    url(r'^gobernacion/$','gobernacion', name='ogcs-mantenimiento-gobernacion'),       
    url(r'^dependencias/json/$','jsondependencia', name='ogcs-dependencia-jsondependencia'),
)
