from django.conf.urls import patterns, url
from .views import HomeView,DocumentView,ChunkView,LoginView,AboutView,UploadView,DashboardView,SearchView, MiniprintJsView, NewCommentView


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^document/(?P<pk>[\d]+)?$', DocumentView.as_view(), name='document'),
    url(r'^document/chunk/(?P<pk>[\d]+)?$', ChunkView.as_view(), name='chunk'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^miniprint.js$', MiniprintJsView.as_view(), name='miniprint_js'),
    url(r'^search/results/$', SearchView.as_view(), name='search'),
    url(r'^comment/chunk/(?P<chunk_id>[\d]+)?/parent/(?P<parent_id>[\d]+)/?$', NewCommentView.as_view(), name='new_comment'),
)
