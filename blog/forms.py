from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {'title':forms.TextInput(attrs=
                {'placeholder':'Enter title...',
                 'style':'width: 100%; padding: 0.5rem; font-size: 1rem; margin-bottom: 1rem; border:1px solid #e5e7eb; border-radius: 6px;'}),
                 'content':forms.Textarea(attrs=
                {'placeholder':'Write your content...',
                 'rows': 6,
                 'style':'width: 100%; padding: 0.5rem; font-size: 1rem; margin-bottom: 1rem; border:1px solid #e5e7eb; border-radius: 6px;'})

        }
        