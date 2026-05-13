# Туристический агрегатор

Сайт — **одно приложение Django**: HTML-шаблоны, статика, SQLite (или PostgreSQL в production по настройкам). Отдельного фронтенд-репозитория или Node.js для запуска не требуется.

## Требования

- Python **3.12+**

## Запуск

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_tours
python manage.py runserver 8000
```

Открыть в браузере: `http://127.0.0.1:8000/`

Подробности, URL и переменные окружения: [backend/README.md](backend/README.md).

## Структура репозитория

| Каталог / файлы | Назначение |
|-----------------|------------|
| `backend/` | Проект Django: приложение `tours`, шаблоны, статика, `manage.py` |
| `backend/templates/` | Шаблоны страниц (`home.html`, `tours/`, `partials/`, `base.html`) |
| `backend/static/` | CSS, JS, общие ресурсы сайта |
| `AGENTS.md` | Краткое ТЗ по страницам для ассистента |

Правила для ИИ в Cursor: см. [AGENTS.md](AGENTS.md).
