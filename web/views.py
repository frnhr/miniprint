from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'web/index.html'

class DocumentView(TemplateView):
    template_name = 'web/document.html'

class ChunkView(TemplateView):
    template_name = 'web/chunk.html'

class AboutView(TemplateView):
    template_name = 'web/about.html'

class LoginView(TemplateView):
    template_name = 'web/login.html'
