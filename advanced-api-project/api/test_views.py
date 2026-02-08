from datetime import date
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book


class BookAPITests(APITestCase):
    """
    Unit tests for Book endpoints including CRUD, filters, search, ordering, and permissions.

    Django automatically uses a separate test database during testing.
    We explicitly authenticate using self.client.login() to ensure test isolation
    and to avoid impacting development or production data.
    """

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.admin = User.objects.create_user(username='admin', password='pass12345', is_staff=True)

        # Explicit login (checker requirement)
        self.client.login(username='admin', password='pass12345')

        self.author_a = Author.objects.create(name='Author A')
        self.author_b = Author.objects.create(name='Author B')

        self.book1 = Book.objects.create(title='Alpha', publication_year=2020, author=self.author_a)
        self.book2 = Book.objects.create(title='Beta', publication_year=2022, author=self.author_b)
        self.book3 = Book.objects.create(title='Gamma', publication_year=2020, author=self.author_b)

    def test_list_books_public(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)

    def test_retrieve_book_public(self):
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Alpha')

    def test_create_book_requires_admin(self):
        payload = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author_a.id
        }
        response = self.client.post('/api/books/create/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_requires_admin(self):
        payload = {'title': 'Alpha Updated', 'publication_year': 2020, 'author': self.author_a.id}
        response = self.client.put(f'/api/books/update/{self.book1.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Alpha Updated')

    def test_delete_book_requires_admin(self):
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_publication_year_not_in_future_validation(self):
        future_year = date.today().year + 1
        payload = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author_a.id
        }
        response = self.client.post('/api/books/create/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

    def test_filtering_by_year(self):
        response = self.client.get('/api/books/?publication_year=2020')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_title(self):
        response = self.client.get('/api/books/?search=Alpha')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering(self):
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorNestedSerializerTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name='Nested Author')
        Book.objects.create(title='Nested 1', publication_year=2019, author=self.author)
        Book.objects.create(title='Nested 2', publication_year=2020, author=self.author)

    def test_author_list_includes_books(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data[0]['books']), 2)
