from django import forms
from .models import Post
from tinymce import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)
    content = forms.CharField(widget=TinyMCEWidget(attrs={'required': False, 'cols': 30, 'rows': 10}))
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'category',
            'description',
            'content',
            'image',
            'draft',
            'publish',
        ]