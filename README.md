# Namitha & Sreeram Wedding Invitation — Django + RSVP Database

## How it works
- `/` — public invitation only. No admin/dashboard link appears on the invitation.
- `/rsvp/submit/` — saves form submissions into the database.
- `/private-rsvp/YOUR_LONG_SECRET_TOKEN/` — private RSVP page showing counts and the submitted fields: name, phone/WhatsApp, number of guests, invited by, attendance, message, and submission time.
- There is no separate admin panel or admin login page in this setup.

## Local setup
1. Install Python 3.11+.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set a private token before running. In PowerShell:
   ```powershell
   $env:RSVP_VIEW_TOKEN = "use-a-long-random-secret-string-here"
   $env:DJANGO_SECRET_KEY = "use-another-long-random-secret"
   ```
   Use long, unique random values; do not publish them or commit them to GitHub.
5. Create database tables:
   ```bash
   python manage.py migrate
   ```
6. Run:
   ```bash
   python manage.py runserver
   ```
7. Public invitation: `http://127.0.0.1:8000/`
8. Private RSVP page: `http://127.0.0.1:8000/private-rsvp/use-a-long-random-secret-string-here/`

The token in the URL must exactly match `RSVP_VIEW_TOKEN`. Keep the full private URL confidential. A token URL is not as strong as individual login accounts: anyone who obtains it can view RSVP details. Use HTTPS in hosting.

## Hosting
Configure these environment variables in the hosting provider:
- `DJANGO_SECRET_KEY` — long random secret
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=your-domain.com,your-hostname`
- `RSVP_VIEW_TOKEN` — long random secret used in the private URL
- `DATABASE_URL` — hosted PostgreSQL URL for persistent production data

Deploy command:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn wedding_project.wsgi:application
```

Use managed PostgreSQL for production. SQLite on ephemeral hosting may lose data after restarts or redeploys.

## RSVP form
The invitation records:
- Full name
- Phone / WhatsApp
- Number of guests (1–20)
- Invited by (Bride's Side, Groom's Side, Family Friend)
- Attendance (accept / decline)
- Optional message

Expected guest total adds the `guests` values for RSVP responses marked attending.
