from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('home.views',
    url(r'^home/','index', name='ogcs-login'),
	# menu home's page	
)
