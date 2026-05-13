# Туристический агрегатор (Frontend + API)

## Стек

- **Frontend:** Next.js (App Router) + Mantine — каталог `frontend/`.
- **Backend:** Django 5 + Django REST Framework — каталог `backend/`, префикс API `/api/`.

Фронтенд по умолчанию ходит в API по **относительному пути `/api`** — Next проксирует запросы на Django (`BACKEND_ORIGIN`, по умолчанию `http://127.0.0.1:8000`). Так каталог работает и с `localhost`, и с IP в LAN.

Опционально:

- **`NEXT_PUBLIC_API_URL`** — если API на другом домене (production или отдельный хост).
- **`API_URL`** — база для серверных запросов Next (карточка тура, блок на главной), по умолчанию `http://127.0.0.1:8000/api`. Задайте, если Django не на localhost.
- **`BACKEND_ORIGIN`** — только для rewrites в `next.config.ts` (куда проксировать `/api`), по умолчанию `http://127.0.0.1:8000`.

```bash
# чаще всего в dev ничего не нужно — только запущенный Django на :8000

# пример: Django на другой машине / в Docker
# BACKEND_ORIGIN=http://host.docker.internal:8000
# API_URL=http://host.docker.internal:8000/api
```

## Требования

- Node.js **22+**, npm **10+**
- Python **3.12+**

## Backend (кратко)

```bash
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_tours
python manage.py runserver 8000
```

Подробности: `backend/README.md`.

## Frontend

```bash
cd frontend
npm install
```

### Переменные

В `frontend/.env.local` обычно **ничего не нужно**: запросы идут на `/api` и проксируются на Django (`BACKEND_ORIGIN`).

Если API на отдельном URL:

```bash
NEXT_PUBLIC_API_URL=https://api.example.com/api
```

### Запуск в режиме разработки

Запуск на порту **3054**:

```bash
cd frontend
npm run dev -- --port 3054
```

Открыть в браузере: `http://localhost:3054`

## Сборка и запуск (production)

```bash
cd frontend
npm run build
npm run start -- --port 3054
```

## Структура

- `frontend/` — Next.js приложение
  - `src/app/` — страницы и layout (App Router)
  - `src/components/` — компоненты (header/footer и далее по блокам)
  - `src/theme.ts` — тема Mantine
- `backend/` — Django API для туров
