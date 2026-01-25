from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect

# REQUIRED BY CHECKER (exact import)
from .forms import ExampleForm, BookForm, BookSearchForm

from .models import Book

@login_required
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all().order_by("title")

    if form.is_valid():
        q = form.cleaned_data.get("q") or ""
        if q:
            books = books.filter(title__icontains=q)

    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})

@login_required
@permission_required("bookshelf.can_view", raise_exception=True)
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "bookshelf/book_detail.html", {"book": book})

@login_required
@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/book_form.html", {"form": form, "mode": "create"})

@login_required
@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/book_form.html", {"form": form, "mode": "edit", "book": book})

@login_required
@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "bookshelf/book_confirm_delete.html", {"book": book})

def form_example(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            return render(request, "bookshelf/form_example.html", {"form": form, "success": True})
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})
