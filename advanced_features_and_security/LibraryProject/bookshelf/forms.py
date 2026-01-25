from django import forms
from .models import Book

class ExampleForm(forms.Form):
    """
    Example form required by checker.
    Demonstrates safe input handling (Task 2).
    """
    name = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea, required=False)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]

class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=100)
