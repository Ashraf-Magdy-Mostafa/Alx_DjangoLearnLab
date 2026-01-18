from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library


# ---------------------------
# Function-Based View (FBV)
# List all books in database
# ---------------------------
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# ---------------------------
# Class-Based View (CBV)
# Show details of one library
# ---------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
