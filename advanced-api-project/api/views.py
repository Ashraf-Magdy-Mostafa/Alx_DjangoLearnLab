from rest_framework import generics
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .permissions import IsAdminOrReadOnly

# =========================
# Generic Views (Task 1)
# =========================
# CRUD using DRF generics with role-based permissions:
# - Read: allowed for everyone
# - Write: only admin/staff users

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
    permission_classes = [IsAdminOrReadOnly]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


# Authors with nested books (Task 0 custom/nested serializer demo)
class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
