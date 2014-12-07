from django.conf.urls import patterns, url
from .views import RemoteScriptView, RemoteCheckView

urlpatterns = patterns('',
    url(r'^check/', RemoteCheckView.as_view(), name='remote_check'),
    url(r'^(?P<document_id>[\d]+)/script.js$', RemoteScriptView.as_view(), name='remote_script_include'),
)
