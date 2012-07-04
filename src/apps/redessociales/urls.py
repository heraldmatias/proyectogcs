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
    url(r'^twitter/diario/edit/(?P<codigo>\d+)/$','twitterdiario_edit', name='ogcs-redes-twitter-diario-edit'), 
    url(r'^twitter/diario/consulta/$','twitterdiario_consulta', name='ogcs-redes-twitter-diario-query'),
    url(r'^twitter/diario/print/$','twitterdiario_print', name='ogcs-redes-twitter-diario-print'),
    url(r'^facebook/$','facebook', name='ogcs-redes-facebook'),
    url(r'^facebook/edit/(?P<codigo>\d+)/$','facebook_edit', name='ogcs-redes-facebook-edit'),    
    url(r'^facebook/consulta/$','facebook_consulta', name='ogcs-redes-facebook-query'),   
    url(r'^facebook/print/$','facebook_print', name='ogcs-redes-facebook-print'),
    url(r'^facebook/diario/$','facebookdiario', name='ogcs-redes-facebook-diario'),
    url(r'^facebook/diario/edit/(?P<codigo>\d+)/$','facebookdiario_edit', name='ogcs-redes-facebook-diario-edit'), 
    url(r'^facebook/diario/consulta/$','facebookdiario_consulta', name='ogcs-redes-facebook-diario-query'),
    url(r'^facebook/diario/print/$','facebookdiario_print', name='ogcs-redes-facebook-diario-print'),
    url(r'^youtube/$','youtube', name='ogcs-redes-youtube'),
    url(r'^youtube/edit/(?P<codigo>\d+)/$','youtube_edit', name='ogcs-redes-youtube-edit'),    
    url(r'^youtube/consulta/$','youtube_consulta', name='ogcs-redes-youtube-query'),   
    url(r'^youtube/print/$','youtube_print', name='ogcs-redes-youtube-print'),
    url(r'^youtube/diario/$','youtubediario', name='ogcs-redes-youtube-diario'),
    url(r'^youtube/diario/edit/(?P<codigo>\d+)/$','youtubediario_edit', name='ogcs-redes-youtube-diario-edit'), 
    url(r'^youtube/diario/consulta/$','youtubediario_consulta', name='ogcs-redes-youtube-diario-query'),
    url(r'^youtube/diario/print/$','youtubediario_print', name='ogcs-redes-youtube-diario-print'),
)
