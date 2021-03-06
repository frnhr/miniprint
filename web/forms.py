from django import forms


class CompanyForm(forms.Form):
    company_name = forms.CharField(label='Company name', max_length=100)


class DocumentUploadForm(forms.Form):
    title = forms.CharField(label='title', max_length=300, required=True)
    text  = forms.CharField(widget=forms.Textarea, required=True)

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


