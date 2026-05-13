# Django API (туры)

## Окружение

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## База и данные

```bash
python manage.py makemigrations tours
python manage.py migrate
python manage.py seed_tours
```

## Запуск

```bash
python manage.py runserver 8000
```

- Список туров: `GET http://127.0.0.1:8000/api/tours/` (query-параметры как в URL каталога на фронте: `q`, `region`, `activity`, `from`, `to`, `priceMin`, `priceMax`, `duration`, `season`, `holiday`, `avail`, `sort`, `dir`).
- Карточка: `GET http://127.0.0.1:8000/api/tours/<slug>/`

Переменные: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `CORS_ALLOWED_ORIGINS` (через запятую, по умолчанию localhost/127.0.0.1 на портах 3000 и 3054).
