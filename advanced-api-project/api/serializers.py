from datetime import date
from rest_framework import serializers
from .models import Author, Book

# =========================
# Serializers
# =========================
# BookSerializer: serializes all fields of Book, and includes custom validation
# to ensure publication_year is not in the future.
#
# AuthorSerializer: includes the Author name plus a nested list of related books.
# The relationship is handled by the Book model's related_name='books'.

class BookSerializer(serializers.ModelSerializer):
    """Serializes Book fields and validates publication_year."""

    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value: int) -> int:
        """Ensure publication_year is not in the future."""
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError('publication_year cannot be in the future.')
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializes Author and nests their related books."""
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
