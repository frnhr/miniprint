from django.views.generic.base import TemplateView


class RemoteScriptView(TemplateView):
    template_name = 'remote/script.js'
    content_type = 'application/x-javascript'

    def get_context_data(self, **kwargs):
        context = super(RemoteScriptView, self).get_context_data(**kwargs)
        context['checkbox_name'] = self.request.GET.get('checkbox_name', 'false')
        if context['checkbox_name'].lower() == 'false':
            context['checkbox_name'] = False
        return context
