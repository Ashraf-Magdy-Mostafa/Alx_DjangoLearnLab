# Django Blog 📝

A simple blog application built with Django.

## Features
- User authentication: register, login, logout, profile
- Blog posts: CRUD with permissions (only author can edit/delete)
- Comments: add/edit/delete with permissions
- Tags (django-taggit) and search

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Routes
- `/` posts list
- `/posts/new/` create post (login required)
- `/posts/<pk>/` post detail + comments
- `/search/?q=...` search
- `/tags/<tag_name>/` posts by tag
- `/register/`, `/login/`, `/logout/`, `/profile/`
