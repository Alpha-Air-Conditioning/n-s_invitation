import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-this-before-deploying")
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [
    f"https://{h.strip()}" for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip() and h.strip() != "*"
] + ["https://*.vercel.app", "https://*.now.sh", "http://127.0.0.1", "http://localhost"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "wedding",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "wedding_project.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "wedding_project.wsgi.application"

db_url = os.environ.get("DATABASE_URL", "")
is_sqlite = not db_url or "sqlite" in db_url

if is_sqlite and os.environ.get("VERCEL"):
    sqlite_path = Path("/tmp/db.sqlite3")
else:
    sqlite_path = BASE_DIR / "db.sqlite3"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{sqlite_path}",
        conn_max_age=600,
        ssl_require=False if is_sqlite else (not DEBUG),
    )
}
if "sqlite" in DATABASES["default"]["ENGINE"] and "sslmode" in DATABASES["default"].get("OPTIONS", {}):
    DATABASES["default"]["OPTIONS"].pop("sslmode", None)

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
RSVP_VIEW_TOKEN = os.environ.get("RSVP_VIEW_TOKEN", "hsiaAjiOD064kDaD-MZrKAlH702slO8_").strip()
LOGIN_URL = "/accounts/login/"
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
X_FRAME_OPTIONS = "DENY"
