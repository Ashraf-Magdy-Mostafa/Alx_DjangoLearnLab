from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer

# =========================
# Generic Views (Task 1)
# =========================
# We implement CRUD using DRF generics:
# - List all books
# - Retrieve a single book
# - Create a new book
# - Update a book
# - Delete a book
#
# Permissions:
# - Unauthenticated users can read (GET)
# - Authenticated users can create/update/delete

class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer

    # Task 2: filtering, searching, ordering
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Extra: Author list/detail with nested books (Task 0 custom/nested serializer demo)

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
