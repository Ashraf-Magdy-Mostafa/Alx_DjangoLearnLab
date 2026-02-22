# Social Media API (Django + DRF)

This project implements a Social Media API with:
- ✅ Custom User (bio, profile_picture, following/followers)
- ✅ Token Authentication (register/login returns token)
- ✅ Posts + Comments CRUD with owner-only edit/delete
- ✅ Follows + Feed (posts from followed users)
- ✅ Likes + Notifications (new follower, like, comment)
- ✅ Production-ready basics (Gunicorn + WhiteNoise + env config)

---

## 1) Setup (Local)

```bash
cd social_media_api
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` (optional), then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Admin: `http://127.0.0.1:8000/admin/`

---

## 2) API Auth

Base path:
- `http://127.0.0.1:8000/api/`

### Register (returns token)
`POST /api/accounts/register/`
```json
{ "username":"ashraf", "password":"pass1234", "email":"a@b.com" }
```

### Login (returns token)
`POST /api/accounts/login/`
```json
{ "username":"ashraf", "password":"pass1234" }
```

Use the token:
```bash
curl -H "Authorization: Token <TOKEN>" http://127.0.0.1:8000/api/accounts/profile/
```

---

## 3) Core Endpoints (Summary)

### Accounts
- `POST  /api/accounts/register/`
- `POST  /api/accounts/login/`
- `GET   /api/accounts/profile/`
- `PATCH /api/accounts/profile/`
- `POST  /api/accounts/follow/<user_id>/`
- `POST  /api/accounts/unfollow/<user_id>/`

### Posts & Comments
- `GET/POST     /api/posts/posts/`
- `GET/PATCH/DELETE /api/posts/posts/<id>/`
- `GET/POST     /api/posts/comments/`  (filter by `?post=<post_id>`)
- `GET/PATCH/DELETE /api/posts/comments/<id>/`
- `GET          /api/posts/feed/`
- `POST         /api/posts/posts/<id>/like/`
- `POST         /api/posts/posts/<id>/unlike/`

### Notifications
- `GET /api/notifications/notifications/` (optional filter: `?unread=true`)
- `POST /api/notifications/notifications/mark_all_read/`

---

## 4) Filtering, Search & Pagination

Posts support:
- Search: `GET /api/posts/posts/?search=django`
- Ordering: `GET /api/posts/posts/?ordering=-created_at`

Pagination is enabled globally (page size = 10).

---

## 5) Deployment Notes (Basic)

- Uses `dj-database-url` for `DATABASE_URL`
- Uses WhiteNoise for static files
- `Procfile` included for Heroku-like platforms

Typical env vars:
- `DEBUG=False`
- `SECRET_KEY=...`
- `ALLOWED_HOSTS=your-domain.com`
- `DATABASE_URL=postgres://...`

