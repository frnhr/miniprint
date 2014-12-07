from django.conf.urls import patterns, url
from .views import VoteChunk, VoteComment


urlpatterns = patterns('',
    url(r'^vote/chunk/?$', VoteChunk.as_view(), name='vote_chunk_api'),
    url(r'^vote/comment/?$', VoteComment.as_view(), name='vote_comment_api'),
)
