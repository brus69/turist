# Туристический агрегатор

Сайт отдаётся **одним приложением Django** (HTML-шаблоны + статика). Каталог **`frontend/`** сохранён как **архив** прежней вёрстки на Next.js/React и **не требуется** для запуска.

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

Подробности и список URL: [backend/README.md](backend/README.md).

## Структура

- `backend/` — Django: модели туров, шаблоны в `backend/templates/`, CSS в `backend/static/css/`
- `frontend/` — архив (Next.js + Mantine), не используется в продакшен-потоке проекта
