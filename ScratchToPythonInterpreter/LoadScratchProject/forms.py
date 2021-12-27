from django import forms


class ProjectForm(forms.Form):
    project = forms.FileField(label="", widget=forms.FileInput(attrs={'class': "form-control col-8"}))
    #project_id = forms.CharField(max_length=20, label='', widget=forms.TextInput(
    #   attrs={'class': "form-control col-8", 'placeholder': "Podaj id projektu", 'aria-label': "Podaj id projektu"}))