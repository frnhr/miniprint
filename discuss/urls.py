from django.conf.urls import patterns, url
from .views import VoteChunk


urlpatterns = patterns('',
    url(r'^vote/chunk/?$', VoteChunk.as_view(), name='vote_chunk_api'),
)
