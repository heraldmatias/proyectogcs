# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),    
    # grapelli admin urls
    (r'^grappelli/', include('grappelli.urls')),
    (r'^foro/', include('pybb.urls', namespace='pybb')),
    # urls
    (r'^chat/', include('jqchat.urls')),
    (r'^$', 'home.views.index'),
    (r'^home/', include('home.urls')),
    (r'^ubigeo/', include('ubigeo.urls')),
    (r'^dependencia/', include('dependencia.urls')),
    (r'^mantenimiento/', include('usuario.urls')),
    (r'^redessociales/', include('redessociales.urls')),
    (r'^usuario/', include('usuario.urls')),
    (r'^extras/', include('extras.urls')),
)

#if settings.DEBUG:
from django.views.static import serve
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$',
        serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^static/(?P<path>.*)$',
        serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^favicon\.ico$', 
        'django.views.generic.simple.redirect_to', 
        {'url': '/static/images/favicon.ico'}),
)

