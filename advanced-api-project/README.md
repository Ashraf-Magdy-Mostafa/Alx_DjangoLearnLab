# Advanced API Development with Django REST Framework

This project demonstrates advanced DRF concepts:
- Custom serializers (nested relationships)
- DRF generic views for CRUD
- Filtering, searching, and ordering
- Unit tests for API behavior

## Setup

```bash
pip install django djangorestframework django-filter
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Endpoints

### Books (Generic Views)
- `GET  /api/books/` (list, supports filter/search/order)
- `GET  /api/books/<id>/` (detail)
- `POST /api/books/create/` (create - authenticated)
- `PUT  /api/books/<id>/update/` (update - authenticated)
- `DELETE /api/books/<id>/delete/` (delete - authenticated)

### Authors (Nested books in response)
- `GET /api/authors/`
- `GET /api/authors/<id>/`

## Filtering, Searching, Ordering Examples

- Filter by year: `/api/books/?publication_year=2020`
- Search: `/api/books/?search=Alpha`
- Order by year desc: `/api/books/?ordering=-publication_year`

## Run Tests

```bash
python manage.py test api
```
