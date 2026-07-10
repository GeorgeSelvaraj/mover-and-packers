     
# Movers & Packers

A Django-based web application for a Packers & Movers company. It includes a public-facing website (services, about, contact, request a quote) and a full admin dashboard for managing services, bookings, field agents, customer queries, reports, and admin users.

---

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python 3.9, Django 4.2 |
| Database | SQLite (`db.sqlite3`) |
| Frontend | Django Templates, Bootstrap 4.5, jQuery 3.5, Font Awesome 5/6 |
| Tables/Charts | DataTables 1.10 (with Buttons + jszip + pdfmake), Chart.js |
| Fonts | Google Fonts — Inter, Outfit, Space Grotesk |
| Auth | Django built-in `auth_user` (custom multi-admin layer) |

---

## Features

### Public website
- Landing page, About, Services listing, Contact form
- "Request a Quote" form that creates a booking record and links it to a service

### Admin dashboard
- Login (staff-only)
- Animated KPI dashboard (Services, Queries, Bookings) with Chart.js charts
- **Services** — add / edit / delete with image and price
- **Bookings**
  - New Bookings (status pending) and Old Bookings (status completed)
  - Booking detail / edit page with route, items, payment, agent assignment
  - Payment fields: total amount, advance paid, payment status (Pending / Partial / Completed)
- **Agents** (admin tab)
  - Add / list / search / delete agents
  - Active / inactive flag
  - Assign an agent to any booking from the booking edit page
  - Agent name shown in new/old booking lists
- **Queries (Contact messages)**
  - Unread vs Read
  - Mark-as-read on view, reply via edit
- **Search** — global search across queries and bookings
- **Reports** — date-range report of bookings/queries/services
- **Change Password** — for the logged-in admin (uses Django's `PasswordChangeForm` with `update_session_auth_hash`)
- **Admin Users** (super-admin only)
  - Create new admins (staff or super-admin)
  - Reset another admin's password
  - Enable / disable / delete other admins (cannot act on yourself)
  - Passwords validated against `AUTH_PASSWORD_VALIDATORS`

---

## Project structure

```
MoversAndPackers/
├── manage.py
├── db.sqlite3
├── media/                       # uploaded service images
├── env/                         # local virtualenv (not committed)
├── MoversAndPackers/            # Django project package
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── moverspackers/               # main app
    ├── models.py                # SiteUser, Services, Contact, Agent
    ├── views.py                 # all view functions
    ├── admin.py                 # Django-admin model registration
    ├── apps.py
    ├── tests.py
    ├── migrations/
    ├── static/
    │   ├── css/                 # sidebar.css, mystyle.css, login.css
    │   ├── js/
    │   └── images/
    └── templates/
        ├── admin_base.html      # shared admin layout (sidebar + topbar)
        ├── admin_login.html
        ├── admin_home.html      # dashboard
        ├── add_services.html / manage_services.html / edit_service.html
        ├── new_booking.html / old_booking.html / view_bookingdetail.html
        ├── agents.html
        ├── unread_queries.html / read_queries.html / view_queries.html
        ├── change_password.html
        ├── manage_admins.html / reset_admin_password.html
        ├── search.html
        ├── booking_report.html
        └── index.html / about.html / contact.html / services.html / request_quote.html / registration.html
```

---

## Data models

All models live in `moverspackers/models.py`.

### `SiteUser` (booking)
| Field | Type | Notes |
|---|---|---|
| name, email, mobile | Char | customer |
| location, shiftingloc | Char | from / to address |
| shiftingdate | Date | requested moving date |
| briefitems, items | Char / Text | items to move |
| requestdate | DateTime | when the quote was submitted |
| service | FK → `Services` | which service was requested |
| total_amount, advance_paid | Float | money |
| payment_status | Char(choices) | Pending / Partial / Completed |
| assigned_agent | FK → `Agent` | who is handling this booking |
| status | Char | `None` = new booking, `"1"` = old/completed |
| remarks, updatedate | Char / DateTime | admin notes |

### `Services`
title, description, image, price, creationdate.

### `Agent`
name, mobile, email, address, is_active, creationdate.

### `Contact`
Customer-submitted query: name, contact_no, email, subject, message, messagedate, isread.

Admin users use Django's built-in `auth_user` table — admins are users with `is_staff=True`; super-admins additionally have `is_superuser=True`.

---

## URL map

| URL | Name | Purpose |
|---|---|---|
| `/` | `index` | public home |
| `/about/` | `about` | about page |
| `/services/` | `services` | public services list |
| `/request_quote/` | `request_quote` | public quote form |
| `/contact/` | `contact` | public contact form |
| `/admin_login/` | `admin_login` | admin login |
| `/admin_home/` | `admin_home` | admin dashboard |
| `/logout/` | `logout` | logout |
| `/change_password/` | `change_password` | self-service password change |
| `/manage_admins/` | `manage_admins` | super-admin: list + add admins |
| `/delete_admin/<id>/` | `delete_admin` | super-admin: delete an admin (POST) |
| `/toggle_admin/<id>/` | `toggle_admin` | super-admin: enable/disable an admin (POST) |
| `/reset_admin_password/<id>/` | `reset_admin_password` | super-admin: reset another admin's password |
| `/add_services/` `/manage_services/` `/edit_service/<id>/` `/delete_service/<id>/` | services CRUD |
| `/agents/` `/delete_agent/<id>/` | agents CRUD + assignment |
| `/new_booking/` `/old_booking/` `/view_bookingdetail/<id>/` `/delete_booking/<id>/` | bookings |
| `/unread_queries/` `/read_queries/` `/view_queries/<id>/` `/delete_query/<id>/` | queries |
| `/search/` | `search` | global search |
| `/booking_report/` | `booking_report` | date-range reports |
| `/admin/` | Django built-in admin |

---

## Getting started (local development)

### 1. Prerequisites
- Python 3.9+
- pip / venv

### 2. Clone and create a virtualenv

```bash
cd "MoversAndPackers"
python3 -m venv env
source env/bin/activate         # macOS / Linux
# env\Scripts\activate          # Windows
```

### 3. Install dependencies

This repo doesn't ship a `requirements.txt` yet. Install Django explicitly:

```bash
pip install "Django>=4.2,<5"
```

(Optional: freeze your env with `pip freeze > requirements.txt`.)

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create the first super-admin

```bash
python manage.py createsuperuser
```

This is required so you can log in to `/admin_login/` and use the `Admin Users` tab to create more admins from the UI afterwards.

### 6. Run the dev server

```bash
python manage.py runserver
```

Open:
- Public site: <http://127.0.0.1:8000/>
- Admin dashboard: <http://127.0.0.1:8000/admin_login/>
- Django built-in admin: <http://127.0.0.1:8000/admin/>

---

## Common workflows

### Add an admin
1. Log in as a super-admin.
2. Click **Admin Users** in the sidebar.
3. Fill the form on the left. Tick **Grant super admin** if they should manage other admins.

### Assign an agent to a booking
1. Add agents under **Agents**.
2. Open any booking in **New Bookings → View / Edit**.
3. Pick an agent from the **Assigned Agent** dropdown and Save.

### Mark a booking complete
Saving from the booking edit form sets `status="1"`, which moves it to **Old Bookings**.

### Generate a report
**Reports → Booking Dates** — pick module + date range, export from DataTables buttons (CSV / Excel / PDF / Print).

---

## Configuration

Most settings live in `MoversAndPackers/settings.py`.

- `DEBUG = True` — disable for production.
- `SECRET_KEY` — replace before deployment (currently the default `django-insecure-...`).
- `ALLOWED_HOSTS = []` — populate before deployment.
- `DEFAULT_AUTO_FIELD = "django.db.models.AutoField"` — kept on `AutoField` to match the existing schema.
- `MEDIA_URL = "/media/"`, `MEDIA_ROOT = BASE_DIR/"media"` — uploaded files (service images).
- `STATIC_URL = "/static/"` — app static assets under `moverspackers/static/`.
- `AUTH_PASSWORD_VALIDATORS` — validates passwords for change-password and reset-password flows.

---

## Testing & checks

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

The repo currently has no unit tests in `tests.py`.

---

## Production checklist (before deploying)

- [ ] `DEBUG = False`
- [ ] Set a real `SECRET_KEY` (50+ chars, random)
- [ ] Populate `ALLOWED_HOSTS`
- [ ] Move secrets to environment variables (e.g. `django-environ`)
- [ ] Switch DB from SQLite to Postgres / MySQL
- [ ] Configure HTTPS:
  - `SECURE_SSL_REDIRECT = True`
  - `SESSION_COOKIE_SECURE = True`
  - `CSRF_COOKIE_SECURE = True`
  - `SECURE_HSTS_SECONDS` (carefully)
- [ ] Run `python manage.py collectstatic` and serve via WhiteNoise / CDN / Nginx
- [ ] Run with Gunicorn / uWSGI behind Nginx, not `runserver`
- [ ] Set up scheduled DB backups
- [ ] Replace GET-based `delete_*` links with POST forms (already done for `delete_admin`/`toggle_admin`)

---

## Roadmap ideas

- Booking status workflow: `Pending → Assigned → In Transit → Completed → Cancelled`
- Agent dashboard / login (limited role)
- Email + SMS notifications on booking assignment
- Online advance payment via Razorpay / Stripe
- Customer accounts and a public booking-tracking page
- Invoice PDF generation
- Pagination + filters on bookings list
- Revenue and agent-performance reports

---

## License

Internal / proprietary. Add a license here if you intend to open-source it.
