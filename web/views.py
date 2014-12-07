from django.views.generic import TemplateView
from discuss.models import Comment


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


class DocumentView(TemplateView):
    template_name = 'web/document.html'


class ChunkView(TemplateView):
    template_name = 'web/chunk.html'


class AboutView(TemplateView):
    template_name = 'web/about.html'


class LoginView(TemplateView):
    template_name = 'web/login.html'
