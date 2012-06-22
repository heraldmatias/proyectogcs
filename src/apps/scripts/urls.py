# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('scripts.scripts',   
    url(r'^ogcs/descarga/$','descargar', name='ogcs-descarga'),    
)
