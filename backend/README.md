# Django — сайт на шаблонах

Серверный HTML (Django Templates), туры в SQLite по умолчанию. **REST API и отдельный JS/Node-фронт не используются** — весь публичный сайт рендерится Django.

## Структура `backend/`

| Путь | Назначение |
|------|------------|
| `config/` | Настройки (`settings`, корневые `urls`) |
| `tours/` | Модели туров, админка, фильтры каталога, представления, сиды |
| `templates/` | Шаблоны (`base.html`, `home.html`, `tours/`, `partials/`) |
| `static/` | CSS (`css/site.css`), JS для календаря слотов и админки |
| `manage.py` | Точка входа Django |

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
| `/admin/` | Админка Django |

Переменные: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`.

Статика разработки: `STATICFILES_DIRS` → `backend/static/`. Для production: `collectstatic` и раздача через веб-сервер.
