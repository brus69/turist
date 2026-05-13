"""
Продакшен: DEBUG выключен, STATIC_ROOT для collectstatic, хосты и БД из окружения.

Запуск: DJANGO_SETTINGS_MODULE=config.settings.production
"""

import os
import re
from urllib.parse import unquote

from .base import *  # noqa: F403

DEBUG = False

_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "").strip()
if _hosts:
    ALLOWED_HOSTS = [h.strip() for h in _hosts.split(",") if h.strip()]

if not os.environ.get("DJANGO_SECRET_KEY"):
    raise ValueError("В продакшене задайте переменную окружения DJANGO_SECRET_KEY.")

STATIC_ROOT = BASE_DIR / "staticfiles"

_pg = re.match(
    r"^postgres(?:ql)?://([^:]+):([^@]+)@([^/:]+)(?::(\d+))?/([^?]+)",
    os.environ.get("DATABASE_URL", ""),
)
if _pg:
    user, password, host, port, name = _pg.groups()
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": unquote(name),
            "USER": unquote(user),
            "PASSWORD": unquote(password),
            "HOST": host,
            "PORT": port or "5432",
            "CONN_MAX_AGE": int(os.environ.get("DJANGO_DB_CONN_MAX_AGE", "60")),
        }
    }
