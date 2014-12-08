from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from discuss.models import Comment
from .forms import CompanyForm, DocumentUploadForm, CommentForm
from users.models import Company
from fineprint.models import Document, Chunk
import datetime
from django.core.urlresolvers import reverse, reverse_lazy


class TwitterLoginRequired(object):
    anonymous_template_name = 'web/anonymous.html'

    # subclasses specify:
    request = None
    template_name = None

    def get_template_names(self):
        if not self.request.user.is_authenticated():
            return self.anonymous_template_name
        return self.template_name


class VotedDataMixin(object):
    def get_context_data(self, **kwargs):
        context = super(VotedDataMixin, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['voted_chunks_up'] = (
                self.request.user.chunk_votes
                .filter(score=1)
                .values_list('target_id', flat=True)
            )
            context['voted_chunks_down'] = (
                self.request.user.chunk_votes
                .filter(score=-1)
                .values_list('target_id', flat=True)
            )
            context['voted_comments_up'] = (
                self.request.user.comment_votes
                .filter(score=1)
                .values_list('target_id', flat=True)
            )
            context['voted_comments_down'] = (
                self.request.user.comment_votes
                .filter(score=-1)
                .values_list('target_id', flat=True)
            )
        return context


class SearchFormMixin(FormView):
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        context = super(SearchFormMixin, self).get_context_data(**kwargs)
        if not context.get('form', None):
            context['form'] = self.form_class()
        return context




class SearchView(TwitterLoginRequired, SearchFormMixin):
    template_name = 'web/search_results.html'
    success_url = '/search/results/'

    def form_valid(self, form):
        company_name = form.cleaned_data['company_name']
        results = Company.objects.filter(name__icontains=company_name)
        return self.render_to_response(self.get_context_data(form=form, results=results))


class HomeView(SearchFormMixin, TwitterLoginRequired, TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['trending'] = Comment.get_trending()
        context['home'] = True
        return context


class DocumentView(VotedDataMixin, DetailView):
    model = Document
    template_name = 'web/document.html'
    template_name_field = 'document'

    def get_context_data(self, **kwargs):
        context = super(DocumentView, self).get_context_data(**kwargs)
        context['scoring_enabled'] = False if 'remote' in self.request.GET else True
        context['extends_template_name'] = 'web/main_popup.html' if 'remote' in self.request.GET else 'web/main.html'
        return context


class ChunkView(TwitterLoginRequired, VotedDataMixin, DetailView):
    template_name = 'web/chunk.html'
    template_name_field = 'chunk'
    model = Chunk


class AboutView(TemplateView):
    template_name = 'web/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['about'] = True
        return context


class LoginView(TemplateView):
    template_name = 'web/login.html'


class MiniprintJsView(TemplateView):
    template_name = 'web/miniprint.js'
    content_type = 'text/javascript'


class UploadView(TwitterLoginRequired, FormView):
    template_name = 'web/upload.html'
    success_url = reverse_lazy('dashboard')
    form_class = DocumentUploadForm

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        company = Company.objects.get_or_create(user=self.request.user)[0]  # (obj, created)[0]
        title = form.cleaned_data['title'].capitalize()
        new_document = Document(company=company, title=title)
        new_document.save()
        new_document.parse_input(form.cleaned_data['text'])
        return super(UploadView, self).form_valid(form)


class DashboardView(TwitterLoginRequired, FormView):
    template_name = 'web/dashboard.html'
    success_url = reverse_lazy('dashboard')
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        try:
            context['company'] = self.request.user.company
        except:
            context['company'] = None
        if context['company']:
            context['documents'] = self.request.user.company.get_documents()
        context['dashboard'] = True
        return context

    def form_valid(self, form):
        company_name = form.cleaned_data['company_name'].capitalize()
        new_company = Company(user=self.request.user, name=company_name)
        new_company.save()
        return super(DashboardView, self).form_valid(form)


class NewCommentView(TwitterLoginRequired, FormView):
    template_name = 'web/new_comment.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(NewCommentView, self).get_context_data(**kwargs)
        parent_id = int(self.kwargs['parent_id'])
        chunk_id = int(self.kwargs['chunk_id'])
        context['form'] = CommentForm()

        if parent_id:
            parent = Comment.objects.get(id=parent_id)
            context['text'] = parent.text
        else:
            chunk = Chunk.objects.get(id=chunk_id)
            context['chunk'] = chunk

        return context

    def form_valid(self, form):
        parent_id = int(self.kwargs['parent_id'])
        chunk_id = int(self.kwargs['chunk_id'])
        text = form.cleaned_data['text']

        new_comment = Comment()

        if parent_id:
            parent  = Comment.objects.get(id=parent_id)
        else:
            parent  = None

        new_comment.parent  = parent
        chunk   = Chunk.objects.get(id=chunk_id)
        new_comment.chunk = chunk

        new_comment.user = self.request.user
        new_comment.text = text
        new_comment.timestamp = datetime.datetime.now()
        new_comment.save()

        return super(NewCommentView, self).form_valid(form)

    def get_success_url(self):
        chunk_id = int(self.kwargs['chunk_id'])
        return reverse('chunk', args=(chunk_id,))
