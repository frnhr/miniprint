from django.contrib import admin
from .models import CommentVote, ChunkVote

admin.site.register(CommentVote)
admin.site.register(ChunkVote)
