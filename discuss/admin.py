from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import CommentVote, ChunkVote, Comment
from utils.admin import admin_register


class CommentAdmin(MPTTModelAdmin):
    model = Comment
    list_display = ('__unicode__', 'discuss_score', 'chunk', 'chunk_document', 'chunk_company', )
    mptt_indent_field = '__unicode__'

    def chunk_document(self, obj):
        if not obj or not obj.chunk:
            return ''
        return obj.chunk.document

    def chunk_company(self, obj):
        document = self.chunk_document(obj)
        if not document:
            return ''
        return document.company


class ChunkVoteAdmin(admin.ModelAdmin):
    model = ChunkVote
    list_display = ('id', 'score', 'user', 'target', 'target_id', )
    list_filter = ('target', )

    def target_id(self, obj):
        return obj.target.id


class CommentVoteAdmin(admin.ModelAdmin):
    model = CommentVote
    list_display = ('id', 'score', 'user', 'target', 'target_id', )
    list_filter = ('target', )

    def target_id(self, obj):
        return obj.target.id


admin_register(CommentAdmin)
admin_register(ChunkVoteAdmin)
admin_register(CommentVoteAdmin)


