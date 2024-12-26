from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="Upload Excel File")

from django import forms
from .models import Results

class ResultForm(forms.ModelForm):
    class Meta:
        model = Results
        fields = ['title']  # Add other fields you may need
