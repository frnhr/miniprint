from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from discuss.models import Comment
from fineprint.models import Document


class TwitterLoginRequired(object):
    anonymous_template_name = 'web/anonymous.html'

    # subclasses specify:
    request = None
    template_name = None

    def get_template_names(self):
        if not self.request.user.is_authenticated():
            return self.anonymous_template_name
        return self.template_name


class HomeView(TwitterLoginRequired, TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['trending'] = Comment.get_trending()
        return context


class DocumentView(DetailView):
    model = Document
    template_name = 'web/document.html'
    template_name_field = 'document'

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['voted_chunks_up'] = self.request.user.chunk_votes.filter(score=1).values_list('target_id', flat=True)
            context['voted_chunks_down'] = self.request.user.chunk_votes.filter(score=-1).values_list('target_id', flat=True)
            context['voted_comments_up'] = self.request.user.comment_votes.filter(score=1).values_list('target_id', flat=True)
            context['voted_comments_down'] = self.request.user.comment_votes.filter(score=-1).values_list('target_id', flat=True)
        return context


class ChunkView(TemplateView):
    template_name = 'web/chunk.html'


class AboutView(TemplateView):
    template_name = 'web/about.html'


class LoginView(TemplateView):
    template_name = 'web/login.html'

class UploadView(TemplateView):
    template_name = 'web/upload.html'

class MiniprintJsView(TemplateView):
    template_name = 'web/miniprint.js'
    content_type = 'text/javascript'