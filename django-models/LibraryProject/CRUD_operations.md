# CRUD Operations for Book Model (Django Shell)

## Create
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book
```
# Expected output:
# <Book: 1984>


## Retrieve
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.id, book.title, book.author, book.publication_year
```
# Expected output:
# (1, '1984', 'George Orwell', 1949)


## Update
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
```
# Expected output:
# <Book: Nineteen Eighty-Four>


## Delete
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
```
# Expected output:
# <QuerySet []>
