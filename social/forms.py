from django import forms
from django.forms import widgets

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "author",
            "title",
            "content",
        )
        widgets = {"author": forms.HiddenInput()}