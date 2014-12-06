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
