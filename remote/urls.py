from django.conf.urls import patterns, url
from .views import RemoteScriptView

urlpatterns = patterns('',
    url(r'^(?P<document_id>[\d]+)/script.js$', RemoteScriptView.as_view(), name='remote_script_include'),
)
