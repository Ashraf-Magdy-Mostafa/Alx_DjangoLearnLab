# Advanced API Development with Django REST Framework

Includes:
- Custom serializers (nested Author -> Books)
- Generic CRUD views for Book
- Filtering, searching, ordering on Book list
- Role-based permissions (admin/staff write, public read)
- Unit tests in `api/test_views.py`

## Setup

```bash
pip install django djangorestframework django-filter
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Key URLs

- GET  /api/books/
- GET  /api/books/<id>/
- POST /api/books/create/
- PUT  /api/books/update/<id>/
- DELETE /api/books/delete/<id>/

## Run Tests

```bash
python manage.py test api
```
