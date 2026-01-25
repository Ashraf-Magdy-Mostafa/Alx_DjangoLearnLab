# Advanced Features and Security (Django)

Directory: `advanced_features_and_security`

## Setup
```bash
python -m venv venv
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Task 0: Custom User Model
- `bookshelf.models.CustomUser` extends `AbstractUser`
- Fields: `date_of_birth`, `profile_photo`
- Manager: `CustomUserManager` with `create_user` and `create_superuser`
- `AUTH_USER_MODEL = "bookshelf.CustomUser"` in settings

## Task 1: Permissions & Groups
Custom permissions on `Book` model:
- `can_view`, `can_create`, `can_edit`, `can_delete`

Views use:
- `@permission_required("bookshelf.can_view", raise_exception=True)` etc.

### Groups (create in Admin)
- **Viewers**: can_view
- **Editors**: can_view, can_create, can_edit
- **Admins**: can_view, can_create, can_edit, can_delete

## Task 2: Security Best Practices
- Settings include:
  - `SECURE_BROWSER_XSS_FILTER = True`
  - `X_FRAME_OPTIONS = "DENY"`
  - `SECURE_CONTENT_TYPE_NOSNIFF = True`
  - `CSRF_COOKIE_SECURE = True`, `SESSION_COOKIE_SECURE = True`
- Forms include `{% csrf_token %}` for POST
- Search uses Django ORM (safe) — no raw SQL
- CSP implemented using `django-csp` middleware

## Task 3: HTTPS & Secure Redirects
- `SECURE_SSL_REDIRECT = True`
- `SECURE_HSTS_SECONDS = 31536000`, include subdomains, preload
- Example Nginx HTTPS config: `deployment/nginx_https_example.conf`
