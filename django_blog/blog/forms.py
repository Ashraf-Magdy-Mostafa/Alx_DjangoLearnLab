from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

class PostForm(ModelForm):
    # taggit can accept comma-separated in one field
    tags = forms.CharField(required=False, help_text="Comma-separated tags, e.g. django, blog")

    class Meta:
        model = Post
        fields = ("title", "content", "tags")

    def save(self, commit=True, author=None):
        post = super().save(commit=False)
        if author is not None:
            post.author = author
        if commit:
            post.save()
            tag_str = self.cleaned_data.get("tags", "")
            tags = [t.strip() for t in tag_str.split(",") if t.strip()]
            post.tags.set(*tags)
            self.save_m2m()
        return post

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {"content": forms.Textarea(attrs={"rows": 4})}
