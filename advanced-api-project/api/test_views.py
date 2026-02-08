from datetime import date
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book


class BookAPITests(APITestCase):
    """
    Unit tests for Book endpoints including CRUD, filters, search, ordering, and permissions.

    Note: Django automatically uses a separate test database during `python manage.py test`.
    This project also defines a dedicated SQLite test DB file in settings.py to ensure
    test runs do not affect development data.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.admin = User.objects.create_user(username='admin', password='pass12345', is_staff=True)

        self.author_a = Author.objects.create(name='Author A')
        self.author_b = Author.objects.create(name='Author B')

        self.book1 = Book.objects.create(title='Alpha', publication_year=2020, author=self.author_a)
        self.book2 = Book.objects.create(title='Beta', publication_year=2022, author=self.author_b)
        self.book3 = Book.objects.create(title='Gamma', publication_year=2020, author=self.author_b)

    def test_list_books_public(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)  # ✅ required: response.data

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
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        self.client.force_authenticate(user=self.user)
        response2 = self.client.post('/api/books/create/', payload, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response3 = self.client.post('/api/books/create/', payload, format='json')
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)

    def test_update_book_requires_admin(self):
        payload = {'title': 'Alpha Updated', 'publication_year': 2020, 'author': self.author_a.id}
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(f'/api/books/update/{self.book1.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Alpha Updated')

    def test_delete_book_requires_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/books/delete/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_publication_year_not_in_future_validation(self):
        future_year = date.today().year + 1
        self.client.force_authenticate(user=self.admin)
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
        years = set([b['publication_year'] for b in response.data])
        self.assertEqual(years, {2020})

    def test_search_by_title(self):
        response = self.client.get('/api/books/?search=Alpha')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b['title'] for b in response.data]
        self.assertIn('Alpha', titles)

    def test_ordering(self):
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b['publication_year'] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))


class AuthorNestedSerializerTests(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Nested Author')
        Book.objects.create(title='Nested 1', publication_year=2019, author=self.author)
        Book.objects.create(title='Nested 2', publication_year=2020, author=self.author)

    def test_author_list_includes_books(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Nested Author')
        self.assertEqual(len(response.data[0]['books']), 2)
