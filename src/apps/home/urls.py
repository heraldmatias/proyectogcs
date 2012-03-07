# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('home.views',
    url(r'^$','index', name='ogcs-login'),
    # menu home's page	
)
