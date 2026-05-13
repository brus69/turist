"""Статический контент главной и фильтров (активности, статьи, отзывы и т.д.).

Регионы для сайта и каталога — модель ``Region`` в БД (см. админку / сиды).
"""

from __future__ import annotations

from urllib.parse import quote


def picsum_image(seed: str, width: int, height: int) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in seed)[:80] or "turist"
    w, h = max(16, min(width, 2000)), max(16, min(height, 2000))
    return f"https://picsum.photos/seed/{quote(safe, safe='')}/{w}/{h}"


ACTIVITIES = [
    {"value": "hike", "label": "Пешие походы"},
    {"value": "kayak", "label": "Сплавы"},
    {"value": "horse", "label": "Конные"},
    {"value": "mountain", "label": "Горные"},
]

DIFFICULTY_LABELS = {
    "easy": "Просто",
    "medium": "Средней сложности",
    "hard": "Сложно",
    "very_hard": "Очень сложно",
}

HOLIDAYS = [
    {"value": "newyear", "label": "Новогодние"},
    {"value": "may", "label": "Майские"},
    {"value": "june", "label": "Июньские"},
    {"value": "feb23", "label": "23 февраля"},
    {"value": "mar8", "label": "8 марта"},
]

SEASONS = [
    {"value": "summer", "label": "Лето"},
    {"value": "winter", "label": "Зима"},
    {"value": "spring", "label": "Весна"},
    {"value": "autumn", "label": "Осень"},
]

ARTICLES = [
    {
        "id": "a1",
        "title": "Как собрать рюкзак в поход",
        "excerpt": "Чеклист вещей для выходного маршрута.",
        "href": "#",
        "image": picsum_image("turist-article-backpack", 900, 540),
    },
    {
        "id": "a2",
        "title": "Сложность маршрутов: что значит 3/5",
        "excerpt": "Разбираем шкалу на примерах.",
        "href": "#",
        "image": picsum_image("turist-article-difficulty", 900, 540),
    },
    {
        "id": "a3",
        "title": "Лучшие направления весной",
        "excerpt": "Куда поехать в мае и июне.",
        "href": "#",
        "image": picsum_image("turist-article-spring", 900, 540),
    },
]

REVIEWS = [
    {
        "id": "r1",
        "author": "Анна К.",
        "rating": 5,
        "text": "Отличная организация и маршрут. Обязательно поеду ещё!",
        "tour_title": "Ястребиное",
    },
    {
        "id": "r2",
        "author": "Дмитрий П.",
        "rating": 5,
        "text": "Инструкторы профессионалы, группа дружная.",
        "tour_title": "Ладожский берег",
    },
    {
        "id": "r3",
        "author": "Елена М.",
        "rating": 4,
        "text": "Красивые виды, чуть устали на второй день — но того стоит.",
        "tour_title": None,
    },
]

TRIP_PHOTOS = [
    {"id": "p1", "src": picsum_image("turist-strip-mountains", 640, 420), "alt": "Горы"},
    {"id": "p2", "src": picsum_image("turist-strip-lake", 640, 420), "alt": "Озеро"},
    {"id": "p3", "src": picsum_image("turist-strip-camp", 640, 420), "alt": "Лагерь"},
    {"id": "p4", "src": picsum_image("turist-strip-snow", 640, 420), "alt": "Снег"},
    {"id": "p5", "src": picsum_image("turist-strip-water", 640, 420), "alt": "Вода"},
    {"id": "p6", "src": picsum_image("turist-strip-cliff", 640, 420), "alt": "Скалы"},
]

WHY_US = [
    {
        "title": "Проверенные маршруты",
        "text": "Собираем предложения от организаторов и проверяем описания.",
    },
    {
        "title": "Прозрачные условия",
        "text": "Сложность, длительность и что включено — до бронирования.",
    },
    {
        "title": "Опытные инструкторы",
        "text": "Показываем состав группы и контакты там, где это уместно.",
    },
    {
        "title": "Поддержка",
        "text": "Поможем подобрать тур под даты и уровень подготовки.",
    },
]

HERO_BG = picsum_image("turist-hero-search-main", 1920, 900)

HEADER_NAV = [
    {"label": "Выбрать тур", "href": "/tours/"},
    {"label": "Направления", "href": "/tours/?view=directions"},
    {"label": "Типы туров", "href": "/tours/?view=types"},
    {"label": "Отзывы", "href": "/#reviews"},
    {"label": "Информация", "href": "/#info"},
]


def reviews_for_tour(tour_title: str) -> list[dict]:
    out = []
    for r in REVIEWS:
        tt = r.get("tour_title")
        if not tt or (tt and tt in tour_title):
            out.append(r)
    return out
