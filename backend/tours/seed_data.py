"""Данные для ``python manage.py seed_tours``.

Галереи туров — демо-кадры с Unsplash (travel / природа). Прямые ссылки на iStock без
лицензии в репозиторий не включаем; при покупке материалов подставьте свои URL в ``images``.
"""

from .models import unsplash_photo_url as img

# Порядок регионов в списках на сайте (остальные получают порядок после этого блока).
REGION_DISPLAY_ORDER = (
    "Россия",
    "Карелия и Ленобласть",
    "Алтай",
    "Кавказ",
    "Байкал",
    "Архангельская область",
)


def region_order_for_seed(name: str) -> int:
    try:
        return REGION_DISPLAY_ORDER.index(name)
    except ValueError:
        return len(REGION_DISPLAY_ORDER) + abs(hash(name)) % 1000


def _slots(*items):
    """Только пары дат ISO (start, end). Подписи и ключи слотов — при сохранении тура."""
    return [{"start": a, "end": b} for (a, b) in items]


def _inst(iid: str, name: str, unsplash_avatar_id: str, page_slug: str, bio: str):
    return [
        {
            "id": iid,
            "name": name,
            "avatarUrl": img(unsplash_avatar_id, 200, 200),
            "slug": page_slug,
            "bio": bio,
        }
    ]


BIO_GEORGY = (
    "Инструктор походных программ Ленобласти и Карелии. "
    "Проводит выходные маршруты и короткие скальные блоки с безопасной страховкой. "
    "Сертификат спасателя, опыт групповых выездов с 2014 года."
)

BIO_MARIA = (
    "Гид и инструктор водных маршрутов. "
    "Спокойно ведёт новичков на каяках и пеших выходного дня. "
    "Фокус на комфорте группы и понятных инструктажах."
)

BIO_ALEXEY = (
    "Горный инструктор, программы с акклиматизацией и работой на высоте. "
    "Опыт высотных лагерей и длительных походов. "
    "Подбирает нагрузку под уровень участников."
)


SEED_TOURS = [
    {
        "slug": "yastrebinoe",
        "title": "Ястребиное. Поход из Петербурга со скалолазанием и тарзанкой",
        "region": "Карелия и Ленобласть",
        "country": "Россия",
        "activity_type": "Пешие походы",
        "activity_kind": "hike",
        "difficulty": "medium",
        "difficulty_score": 3,
        "difficulty_max": 5,
        "distance_km": 25,
        "duration_days": 3,
        "backpack_weight_kg": 16,
        "max_people": 22,
        "price": 7900,
        "old_price": None,
        "currency": "RUB",
        "status_label": "ЧЕРЕЗ 3 ЧАСА",
        "spots_left": None,
        "description": (
            "Трёхдневный поход с элементами скалолазания и тарзанки у озера. "
            "Подходит тем, кто хочет совместить активный отдых и красивые виды Ленобласти."
        ),
        "tags": ["Карелия и Ленобласть", "Россия", "Пешие походы", "На выходные"],
        "images": [
            img("1551632811-561732d1e306"),
            img("1464822759023-fed622ff2c3b"),
            img("1478131143081-80f7f84ca84d"),
            img("1506905925346-21bda4d32df4"),
            img("1483728642381-4961a154ca82"),
            img("1516642497649-77d2f1fd5b2b"),
            img("1454496522488-7a8e488e8606"),
        ],
        "date_slots": _slots(
            ("2026-05-08", "2026-05-10"),
            ("2026-05-15", "2026-05-17"),
        ),
        "program_by_day": [
            {"day": 1, "title": "Сбор и переход", "body": "Встреча в Санкт-Петербурге, трансфер к месту старта, установка лагеря, короткая разминка на скалах."},
            {"day": 2, "title": "Скалы и озеро", "body": "Маршрут вдоль берега, скалолазание с инструктором, свободное время и купание (по погоде)."},
            {"day": 3, "title": "Тарзанка и выход", "body": "Утренняя тарзанка, сбор палаток, возвращение в город."},
        ],
        "included": ["Инструктор", "Страховка на маршруте", "Групповое снаряжение"],
        "not_included": ["Питание", "Личное снаряжение", "Дорога до места встречи"],
        "packing_list": ["Рюкзак 40–60 л", "Спальник", "Коврик", "Термос", "Аптечка"],
        "faq": [{"q": "Нужен ли опыт?", "a": "Достаточно базовой физической формы; инструктор проведёт инструктаж."}],
        "instructors": _inst("i1", "Георгий Айвазошвили", "1507003211189-015e2fc17ecb", "georgy-aivazoshvili", BIO_GEORGY),
        "season": "summer",
        "holiday": ["may"],
        "duration_category": "weekend",
    },
    {
        "slug": "ladoga-coast",
        "title": "Ладожский берег. Пеший поход с палатками из Санкт-Петербурга",
        "region": "Карелия и Ленобласть",
        "country": "Россия",
        "activity_type": "Пешие походы",
        "activity_kind": "hike",
        "difficulty": "medium",
        "difficulty_score": 3,
        "difficulty_max": 5,
        "distance_km": 25,
        "duration_days": 3,
        "backpack_weight_kg": 14,
        "max_people": 18,
        "price": 7900,
        "old_price": None,
        "currency": "RUB",
        "status_label": "ЧЕРЕЗ 3 ЧАСА",
        "spots_left": None,
        "description": "Классический выходной поход вдоль Ладоги с ночёвками в палатках.",
        "tags": ["Карелия и Ленобласть", "Россия", "Пешие походы", "На выходные"],
        "images": [
            img("1439066615861-d1af74d74800"),
            img("1472219721910-d8543c02ede0"),
        ],
        "date_slots": _slots(("2026-05-08", "2026-05-10")),
        "program_by_day": [
            {"day": 1, "title": "Старт", "body": "Выезд из Петербурга, первый лагерь."},
            {"day": 2, "title": "Берег", "body": "Переходы по берегу, виды на воду."},
            {"day": 3, "title": "Финиш", "body": "Выход к транспорту и возвращение."},
        ],
        "included": ["Инструктор", "Карта маршрута"],
        "not_included": ["Питание", "Палатка (можно арендовать)"],
        "packing_list": ["Палатка", "Спальник", "Посуда"],
        "faq": [],
        "instructors": _inst("i1", "Георгий Айвазошвили", "1507003211189-015e2fc17ecb", "georgy-aivazoshvili", BIO_GEORGY),
        "season": "summer",
        "holiday": [],
        "duration_category": "weekend",
    },
    {
        "slug": "dve-usadby",
        "title": "Две усадьбы. Однодневный треккинг в Подмосковье",
        "region": "Московская область",
        "country": "Россия",
        "activity_type": "Пешие походы",
        "activity_kind": "hike",
        "difficulty": "easy",
        "difficulty_score": 2,
        "difficulty_max": 5,
        "distance_km": 21,
        "duration_days": 1,
        "backpack_weight_kg": 8,
        "max_people": 25,
        "price": 3300,
        "old_price": None,
        "currency": "RUB",
        "status_label": "ЧЕРЕЗ 3 ЧАСА",
        "spots_left": None,
        "description": "Однодневный маршрут с посещением двух усадебных парков.",
        "tags": ["Московская область", "Россия", "Пешие походы", "Однодневные"],
        "images": [img("1566073771259-6a85048c0847"), img("1527004013197-404bab667e2d")],
        "date_slots": _slots(("2026-05-08", "2026-05-08")),
        "program_by_day": [{"day": 1, "title": "Маршрут", "body": "Сбор в Москве, переходы, экскурсии."}],
        "included": ["Гид"],
        "not_included": ["Обед"],
        "packing_list": ["Удобная обувь", "Вода"],
        "faq": [],
        "instructors": _inst("i2", "Мария Соколова", "1494790108377-be9c29b29330", "maria-sokolova", BIO_MARIA),
        "season": "spring",
        "holiday": ["may"],
        "duration_category": "oneday",
    },
    {
        "slug": "elbrus-hotel",
        "title": "Восхождение на Эльбрус с проживанием в отеле",
        "region": "Кавказ",
        "country": "Россия",
        "activity_type": "Горные",
        "activity_kind": "mountain",
        "difficulty": "very_hard",
        "difficulty_score": 5,
        "difficulty_max": 5,
        "distance_km": 70,
        "duration_days": 9,
        "backpack_weight_kg": 20,
        "max_people": 12,
        "price": 79900,
        "old_price": 89900,
        "currency": "RUB",
        "status_label": "ЧЕРЕЗ ДЕНЬ",
        "spots_left": 4,
        "description": "Программа восхождения с проживанием в отеле на этапах подготовки.",
        "tags": ["Кавказ", "Россия", "Горные", "Большие (от 5 дней)"],
        "images": [img("1519681393784-d120267933ba"), img("1544197158-b7f2aa32784b")],
        "date_slots": _slots(("2026-05-09", "2026-05-17")),
        "program_by_day": [
            {"day": 1, "title": "Прилёт", "body": "Трансфер, размещение, инструктаж."},
            {"day": 2, "title": "Акклиматизация", "body": "Выходы на средние высоты."},
        ],
        "included": ["Инструкторы", "Проживание по программе", "Групповое снаряжение"],
        "not_included": ["Авиабилеты", "Страховка от несчастных случаев расширенная"],
        "packing_list": ["Высотное снаряжение по списку", "Мембранная одежда"],
        "faq": [{"q": "Нужна ли страховка?", "a": "Да, обязательна — поможем оформить."}],
        "instructors": _inst("i3", "Алексей Вершинин", "1500648769291-c17bf87fedd5", "alexey-vershinin", BIO_ALEXEY),
        "season": "summer",
        "holiday": [],
        "duration_category": "long",
    },
    {
        "slug": "kayak-onega",
        "title": "Сплав на каяках по Онежскому заливу",
        "region": "Карелия и Ленобласть",
        "country": "Россия",
        "activity_type": "Сплавы",
        "activity_kind": "kayak",
        "difficulty": "easy",
        "difficulty_score": 2,
        "difficulty_max": 5,
        "distance_km": 14,
        "duration_days": 2,
        "backpack_weight_kg": 10,
        "max_people": 14,
        "price": 5600,
        "old_price": None,
        "currency": "RUB",
        "status_label": "",
        "spots_left": None,
        "description": "Спокойный водный маршрут для новичков.",
        "tags": ["Карелия и Ленобласть", "Россия", "Сплавы", "На выходные"],
        "images": [img("1544551763-46a013bb70d5"), img("1559827262-dc66d52b19c9")],
        "date_slots": _slots(("2026-05-12", "2026-05-13")),
        "program_by_day": [{"day": 1, "title": "Вода", "body": "Инструктаж и сплав."}],
        "included": ["Каяк", "Жилет"],
        "not_included": ["Питание"],
        "packing_list": ["Смена одежды", "Крем от солнца"],
        "faq": [],
        "instructors": _inst("i2", "Мария Соколова", "1494790108377-be9c29b29330", "maria-sokolova", BIO_MARIA),
        "season": "summer",
        "holiday": [],
        "duration_category": "weekend",
    },
    {
        "slug": "altai-tea",
        "title": "Алтай: горные тропы и чайные домики",
        "region": "Алтай",
        "country": "Россия",
        "activity_type": "Пешие походы",
        "activity_kind": "hike",
        "difficulty": "hard",
        "difficulty_score": 4,
        "difficulty_max": 5,
        "distance_km": 55,
        "duration_days": 7,
        "backpack_weight_kg": 18,
        "max_people": 16,
        "price": 45900,
        "old_price": None,
        "currency": "RUB",
        "status_label": "",
        "spots_left": None,
        "description": "Недельный поход по знаковым местам Алтая.",
        "tags": ["Алтай", "Россия", "Пешие походы", "Большие (от 5 дней)"],
        "images": [img("1501555080752-8d99e2a702dd"), img("1469474968028-56623f04e629")],
        "date_slots": _slots(("2026-06-01", "2026-06-07")),
        "program_by_day": [{"day": 1, "title": "Старт", "body": "Встреча группы."}],
        "included": ["Инструктор", "Питание по программе"],
        "not_included": ["Билеты до Горно-Алтайска"],
        "packing_list": ["Рюкзак", "Спальник"],
        "faq": [],
        "instructors": _inst("i3", "Алексей Вершинин", "1500648769291-c17bf87fedd5", "alexey-vershinin", BIO_ALEXEY),
        "season": "summer",
        "holiday": ["june"],
        "duration_category": "long",
    },
]
