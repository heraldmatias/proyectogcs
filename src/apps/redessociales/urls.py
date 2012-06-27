# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('redessociales.views',    
    url(r'^informacion/$','informacion', name='ogcs-redes-informacion'),    
    url(r'^informacion/edit/(?P<codigo>\d+)/$','informacion_edit', name='ogcs-redes-informacion-edit'),    
    url(r'^informacion/consulta/$','informacion_consulta', name='ogcs-redes-informacion-query'),   
    url(r'^informacion/print/$','informacion_print', name='ogcs-redes-informacion-print'),
    url(r'^twitter/$','twitter', name='ogcs-redes-twitter'),
    url(r'^twitter/edit/(?P<codigo>\d+)/$','twitter_edit', name='ogcs-redes-twitter-edit'),    
    url(r'^twitter/consulta/$','twitter_consulta', name='ogcs-redes-twitter-query'),   
    url(r'^twitter/print/$','twitter_print', name='ogcs-redes-twitter-print'),
    url(r'^twitter/diario/$','twitterdiario', name='ogcs-redes-twitter-diario'),
    url(r'^facebook/$','facebook', name='ogcs-redes-facebook'),
    url(r'^facebook/diario/$','facebookdiario', name='ogcs-redes-facebook-diario'),
)
