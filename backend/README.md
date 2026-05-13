# Django — сайт на шаблонах

Серверный HTML (Django Templates), туры в SQLite, без REST API и без отдельного Node-фронта.

## Окружение

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## База и демо-данные

```bash
python manage.py migrate
python manage.py seed_tours
```

## Запуск

```bash
python manage.py runserver 8000
```

Открыть: `http://127.0.0.1:8000/`

## Страницы (URL)

| URL | Описание |
|-----|----------|
| `/` | Главная |
| `/tours/` | Каталог (фильтры через GET: `q`, `region`, `activity`, `from`, `to`, `priceMin`, `priceMax`, `duration`, `season`, `holiday`, `avail`, `sort`, `dir`) |
| `/tours/<slug>/` | Карточка тура |
| `/cabinet/` … | Личный кабинет (демо-страницы) |
| `/admin/` | Админка Django |

Переменные: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`.

Статика разработки: `STATICFILES_DIRS` → `backend/static/`. Для production: `collectstatic` и раздача через веб-сервер.
