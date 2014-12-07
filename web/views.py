from django.shortcuts import render
from django.views.generic import TemplateView


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

class DocumentView(TemplateView):
    template_name = 'web/document.html'

class ChunkView(TemplateView):
    template_name = 'web/chunk.html'

class AboutView(TemplateView):
    template_name = 'web/about.html'

class LoginView(TemplateView):
    template_name = 'web/login.html'
