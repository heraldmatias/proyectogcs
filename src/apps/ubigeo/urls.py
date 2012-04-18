# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
#(?P<opcion>\w+)
urlpatterns = patterns('ubigeo.views',
    url(r'^region/add/$','regionadd', name='ogcs-mantenimiento-region-add'),
    url(r'^region/edit/(?P<codigo>\d+)/$','regionedit', name='ogcs-mantenimiento-region-edit'),
    url(r'^region/consulta/$','regionquery', name='ogcs-mantenimiento-region-consulta'),
    url(r'^provincia/$','provincia', name='ogcs-mantenimiento-provincia'),
    url(r'^provincia/json/$','jsonprovincia', name='ogcs-provincia-jsonprovincia'),
)
