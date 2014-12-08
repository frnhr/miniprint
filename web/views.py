from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from discuss.models import Comment
from .forms import CompanyForm, DocumentUpload
from users.models import Company
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
        context['scoring_enabled'] = False if 'remote' in self.request.GET else True
        context['extends_template_name'] = 'web/main_popup.html' if 'remote' in self.request.GET else 'web/main.html'
        return context


class ChunkView(TemplateView):
    template_name = 'web/chunk.html'


class AboutView(TemplateView):
    template_name = 'web/about.html'


class LoginView(TemplateView):
    template_name = 'web/login.html'


class MiniprintJsView(TemplateView):
    template_name = 'web/miniprint.js'
    content_type = 'text/javascript'


class UploadView(TwitterLoginRequired, FormView):
    template_name = 'web/upload.html'
    success_url = '/profile/'
    form_class = DocumentUpload

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        return context

    def form_valid(self,form):
        company = self.request.user.company
        title   = form.cleaned_data['title']
        new_document = Document(company=company,title=title)
        new_document.save()
        return super(UploadView, self).form_valid(form)


class ProfileView(TwitterLoginRequired, FormView):
    template_name = 'web/profile.html'
    success_url = '/profile/'
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        try:
            context['company'] = self.request.user.company
        except:
            context['company'] = None
        if context['company']:
            context['documents'] = self.request.user.company.get_documents()
        return context

    def form_valid(self, form):
        company_name = form.cleaned_data['company_name']
        new_company = Company(user=self.request.user, name=company_name)
        new_company.save()
        return super(ProfileView, self).form_valid(form)


class SearchView(FormView):
    template_name = 'web/search_results.html'
    success_url = '/search/results/'
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        company_name = form.cleaned_data['company_name']
        results = Company.objects.filter(name__icontains=company_name)
        return self.render_to_response(self.get_context_data(form=form, results=results))

