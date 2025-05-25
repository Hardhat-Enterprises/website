import os, random, string
from pathlib import Path
from dotenv import load_dotenv, set_key
from django.core.cache.backends.base import InvalidCacheBackendError
from pymemcache.client.base import Client
from corsheaders.defaults import default_headers
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'

if not env_path.exists():
    secret_key = ''.join(random.choice(string.ascii_lowercase) for i in range(50))
    with open(env_path, 'w') as f:
        f.write(f'SECRET_KEY={secret_key}\n')

load_dotenv()

SECRET_KEY = os.environ['SECRET_KEY']
if not SECRET_KEY:
    SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for i in range(32))
    set_key('.env', 'SECRET_KEY', SECRET_KEY)

PRODUCTION = 'RUN_MAIN' not in os.environ
DEBUG = not PRODUCTION

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://localhost:5085']

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ---------------- Idle Session Timeout Configuration ----------------
SESSION_COOKIE_AGE = 300  # 5 minutes
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ---------------- Secure Session Cookie Settings ----------------
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'

# ---------------- CSRF Cookie Security Settings ----------------
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'Strict'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

INSTALLED_APPS = [
    'crispy_forms',
    'tinymce',
    'crispy_bootstrap5',
    'captcha',
    "django_light",
    "core.apps.CustomAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    'django_cron',
    'rest_framework',
    'drf_yasg',
    'home',
    'theme_pixel',
    'corsheaders',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "home.idle.LogoutMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "home.ratelimit_middleware.GlobalLockoutMiddleware",
    "core.middleware.LogRequestMiddleware",
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'xss_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'xss_attempts.log',
        },
    },
    'loggers': {
        'xss_logger': {
            'handlers': ['xss_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

ROOT_URLCONF = "core.urls"

HOME_TEMPLATES = os.path.join(BASE_DIR, 'home', 'templates')

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'home.context_processors.dynamic_page_title',
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DB_ENGINE = os.getenv('DB_ENGINE', None)
DB_USERNAME = os.getenv('DB_USERNAME', None)
DB_PASS = os.getenv('DB_PASS', None)
DB_HOST = os.getenv('DB_HOST', None)
DB_PORT = os.getenv('DB_PORT', None)
DB_NAME = os.getenv('DB_NAME', None)

if DB_ENGINE and DB_NAME and DB_USERNAME:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.' + DB_ENGINE,
            'NAME': DB_NAME,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASS,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        },
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = "home.User"

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Australia/Melbourne"
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'custom_static')
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = '/'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'hardhatcompanywebsite@gmail.com'
EMAIL_HOST_PASSWORD = 'nuje nbmo cfqe skjb'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

MESSAGE_TAGS = {
    messages.ERROR: 'error',
    messages.SUCCESS: 'success'
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': os.getenv('CACHE_LOCATION', '127.0.0.1:11211'),
    }
}

try:
    client = Client(os.getenv('CACHE_LOCATION', '127.0.0.1:11211'))
    client.version()
except (ImportError, InvalidCacheBackendError, ConnectionRefusedError):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

RATELIMIT_ENABLE = True
RATELIMIT_VIEW = 'django_ratelimit.ratelimit_view'
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_SETTINGS = {
    'login': {
        'rate': '5/m',
        'block_expiration': 60,
    },
}

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Django-cron configuration class
# CRON_CLASSES = [
#     'home.tasks.CleanStaleRecordsCronJob',
# ]

CRON_CLASSES = [
    "core.cron.ClearExpiredSessions",
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_django': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_activity.log'),
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'activity.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'audit_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'audit.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_django', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'page_access_logger': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'audit_logger': {
            'handlers': ['audit_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
    'https://hardhatwebdev2024.pythonanywhere.com',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'content-type',
    'authorization',
]
