# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('ubigeo.views',
    url(r'^region/$','region', name='ogcs-mantenimiento-region'),    
)
