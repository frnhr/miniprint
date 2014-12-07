from django.conf.urls import patterns, url
from .views import HomeView,DocumentView,ChunkView,LoginView,AboutView,UploadView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login/$', AboutView.as_view(), name='about'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^document/(?P<document_id>[\d]+)?$', DocumentView.as_view(), name='document'),
    url(r'^document/chunk/(?P<chunk_id>[\d]+)?$', ChunkView.as_view(), name='chunk'),
)
