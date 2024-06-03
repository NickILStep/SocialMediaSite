from django import forms
from .models import Post, Comment

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'content']