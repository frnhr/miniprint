from adminsortable.admin import SortableInlineAdminMixin
from django.contrib import admin
from fineprint.models import Chunk, Document, DocumentAgreement
from utils.admin import admin_register


class ChunkAdmin(admin.ModelAdmin):
    model = Chunk
    list_display = ('__unicode__', 'discuss_score', 'document', )
    list_filter = ('document', )


class ChunkInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Chunk
    extra = 0


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ('title', 'company', )
    list_filter = ('company', )
    inlines = (ChunkInline, )


class DocumentAgreementAdmin(admin.ModelAdmin):
    model = DocumentAgreement
    list_display = ('timestamp', 'document', 'user', )
    list_filter = ('document', 'user', )


admin_register(ChunkAdmin)
admin_register(DocumentAdmin)
admin_register(DocumentAgreementAdmin)
