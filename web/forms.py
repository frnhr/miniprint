from django import forms

class CompanyForm(forms.Form):
    company_name = forms.CharField(label='Company name', max_length=100)

class DocumentUpload(forms.Form):
    title = forms.CharField(label='title', max_length=300)
    text  = forms.CharField(widget=forms.Textarea)


