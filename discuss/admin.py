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


admin_register(CommentAdmin)
admin.site.register(CommentVote)
admin.site.register(ChunkVote)

