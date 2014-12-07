from django.core.urlresolvers import reverse
from django.http.response import JsonResponse
from django.views.generic.base import TemplateView, View
from http_status import HttpResponse
from fineprint.models import Document, DocumentAgreement


class RemoteScriptView(TemplateView):
    template_name = 'remote/script.js'
    content_type = 'application/x-javascript'

    def get_context_data(self, document_id, **kwargs):
        context = super(RemoteScriptView, self).get_context_data(**kwargs)
        context['checkbox_name'] = self.request.GET.get('checkbox_name', 'false')
        if context['checkbox_name'].lower() == 'false':
            context['checkbox_name'] = False
        context['remote_check_url'] = self.request.build_absolute_uri(reverse('remote_check'))
        context['document_id'] = document_id
        return context


class RemoteCheckView(View):
    def get(self, request, *args, **kwargs):
        try:
            self._handle_users(request)
        except:
            raise
            pass  # log error, but always return 200
        response = {}
        status = HttpResponse
        return JsonResponse(response, status=status.status_code)

    def _handle_users(self, request):
        user = request.user
        if not user.is_authenticated():
            return
        document_id = request.GET['document_id']
        document = Document.objects.get(id=document_id)
        val = request.GET['val'] == 'true'
        if val:
            DocumentAgreement.objects.get_or_create(user=user, document=document)
        else:
            DocumentAgreement.objects.filter(user=user, document=document).delete()


