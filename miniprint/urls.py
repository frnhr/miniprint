from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'miniprint.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', include('web.urls')),
    url(r'^discuss/', include('discuss.urls')),
    url(r'^remote/', include('remote.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^twitter/', include('twython_django_oauth.urls')),
)
