from django_filters import rest_framework
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from .permissions import IsAdminOrReadOnly

# =========================
# Generic Views (Task 1)
# =========================
# CRUD using DRF generics with permissions based on user roles:
# - Read endpoints: public (IsAuthenticatedOrReadOnly handles read without login)
# - Write endpoints: authenticated users required (IsAuthenticated) + role restriction (IsAdminOrReadOnly)
#
# Filtering, searching, ordering are enabled on BookListView using:
# - rest_framework.DjangoFilterBackend (django-filter)
# - SearchFilter
# - OrderingFilter

class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # ✅ Integrate filtering/search/ordering
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter, OrderingFilter]

    # ✅ Filter by attributes like title, author, publication_year
    filterset_fields = ['title', 'author', 'publication_year']

    # ✅ Enable search on title and author
    search_fields = ['title', 'author__name']

    # ✅ Configure ordering
    ordering_fields = ['title', 'publication_year', 'author__name']
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# Authors with nested books (Task 0 custom/nested serializer demo)
class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
