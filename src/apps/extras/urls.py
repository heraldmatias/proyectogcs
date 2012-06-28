# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('extras.views',    
    url(r'^documentos/add/$','documentos_add', name='ogcs-mantenimiento-doc-add'),
    url(r'^documentos/consulta/$','documentos_query', name='ogcs-mantenimiento-doc-query'),
    url(r'^documentos/print/$','documentos_print', name='ogcs-mantenimiento-doc-print'),
    url(r'^descarga/(?P<archivoo>[a-zA-Z0-9_./]+)/$','descargar', name='ogcs-descarga'), 
    url(r'^categoria/add/$','categoria_add', name='ogcs-mantenimiento-categoria-add'),
    url(r'^categoria/edit/(?P<codigo>\d+)/$','categoria_edit', name='ogcs-mantenimiento-categoria-edit'),
    url(r'^categoria/consulta/$','categoria_query', name='ogcs-mantenimiento-categoria-query'),   
    url(r'^forum/add/$','forum_add', name='ogcs-mantenimiento-foro-add'),
    url(r'^forum/edit/(?P<codigo>\d+)/$','forum_edit', name='ogcs-mantenimiento-foro-edit'),
    url(r'^forum/consulta/$','forum_query', name='ogcs-mantenimiento-foro-query'),
    url(r'^tema/add/$','tema_add', name='ogcs-mantenimiento-tema-add'),
    url(r'^tema/edit/(?P<codigo>\d+)/$','tema_edit', name='ogcs-mantenimiento-tema-edit'),
    url(r'^tema/consulta/$','tema_query', name='ogcs-mantenimiento-tema-query'),
    url(r'^foros/json/$','json_foros', name='ogcs-foros-jsonforos'),
    url(r'^calendar/$','view_calendar', name='ogcs-calendar'),
)
