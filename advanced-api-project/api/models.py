from django.db import models

# =========================
# Models
# =========================
# Author -> Book is a one-to-many relationship:
# - One Author can have many Books
# - Each Book belongs to exactly one Author
#
# These models provide the data structure used by DRF serializers and views.

class Author(models.Model):
    """Represents an author who can have multiple books."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Represents a book written by an author."""
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
