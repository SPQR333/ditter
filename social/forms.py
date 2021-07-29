from django import forms
from django.forms import fields, widgets

from .models import Avatar, Post


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ("picture",)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("author", "text", "parent")
        widgets = {"author": forms.HiddenInput(), "parent": forms.HiddenInput()}
