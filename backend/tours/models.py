from datetime import date
from urllib.parse import quote

from django.db import models

_MONTH_GEN = (
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
)


def _days_word_ru(n: int) -> str:
    n = abs(int(n)) % 100
    if 11 <= n <= 14:
        return "дней"
    n = n % 10
    if n == 1:
        return "день"
    if 2 <= n <= 4:
        return "дня"
    return "дней"


def first_start_date_from_slots(slots: list | None) -> date | None:
    """Первая дата начала по слотам (для сортировки и денормализации)."""
    if not slots:
        return None
    valid = [s for s in slots if s.get("start") and s.get("end")]
    if not valid:
        return None
    valid.sort(key=lambda s: str(s["start"]))
    try:
        return date.fromisoformat(str(valid[0]["start"])[:10])
    except ValueError:
        return None


def date_summary_from_slots(slots: list | None) -> str:
    """Краткая строка дат для карточки по первому слоту с start/end (ISO)."""
    if not slots:
        return "Даты уточняются"
    valid = [s for s in slots if s.get("start") and s.get("end")]
    if not valid:
        if slots and isinstance(slots[0], dict) and slots[0].get("label"):
            return str(slots[0]["label"])
        return "Даты уточняются"
    valid.sort(key=lambda s: str(s["start"]))
    s0 = valid[0]
    try:
        start = date.fromisoformat(str(s0["start"])[:10])
        end = date.fromisoformat(str(s0["end"])[:10])
    except ValueError:
        return str(s0.get("label") or "Даты уточняются")
    days = (end - start).days + 1
    mg = _MONTH_GEN
    dw = _days_word_ru(days)
    if start == end:
        return f"{start.day} {mg[start.month - 1]} {start.year} - {days} {dw}"
    if start.year == end.year and start.month == end.month:
        return f"с {start.day} по {end.day} {mg[start.month - 1]} {start.year} - {days} {dw}"
    if start.year == end.year:
        return f"с {start.day} {mg[start.month - 1]} по {end.day} {mg[end.month - 1]} {start.year} - {days} {dw}"
    return f"с {start.day} {mg[start.month - 1]} {start.year} по {end.day} {mg[end.month - 1]} {end.year} - {days} {dw}"


def picsum_url(seed: str, width: int = 800, height: int = 520) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in seed)[:80] or "turist"
    w, h = max(16, min(width, 2000)), max(16, min(height, 2000))
    return f"https://picsum.photos/seed/{quote(safe, safe='')}/{w}/{h}"


def unsplash_photo_url(photo_id: str, width: int = 800, height: int = 520) -> str:
    """Демо-изображение с ``images.unsplash.com`` (лицензия Unsplash).

    ``photo_id`` — часть пути после ``photo-`` (цифры и дефис), без префикса ``photo-``.
    Для платных стоков (iStock и т.п.) в код нужно подставлять только свои купленные файлы / CDN.
    """
    pid = "".join(c for c in photo_id if c.isalnum() or c == "-")
    if len(pid) < 8:
        pid = "1506905925346-21bda4d32df4"
    w, h = max(16, min(width, 2000)), max(16, min(height, 2000))
    return f"https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w={w}&h={h}&q=80"


class Region(models.Model):
    """Географический регион (один на тур). Имя совпадает с GET-параметром каталога ``region=``."""

    name = models.CharField("Название", max_length=200, unique=True)
    order = models.PositiveSmallIntegerField("Порядок в списках", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self) -> str:
        return self.name


class Season(models.Model):
    """Справочник сезонов (код совпадает с GET-параметром каталога `season=`)."""

    code = models.CharField("Код", max_length=32, unique=True, db_index=True)
    name = models.CharField("Название", max_length=64)
    order = models.PositiveSmallIntegerField("Порядок в списках", default=0)

    class Meta:
        ordering = ["order", "code"]
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"

    def __str__(self) -> str:
        return self.name


class DurationCategory(models.Model):
    """Категория длительности тура (код — GET `duration=` в каталоге)."""

    code = models.CharField("Код", max_length=32, unique=True, db_index=True)
    name = models.CharField("Название", max_length=120)
    order = models.PositiveSmallIntegerField("Порядок в списках", default=0)

    class Meta:
        ordering = ["order", "code"]
        verbose_name = "Категория длительности"
        verbose_name_plural = "Категории длительности"

    def __str__(self) -> str:
        return self.name


class Tour(models.Model):
    """Тур: основные поля в БД, вложенные структуры — JSON."""

    slug = models.SlugField("Слаг (URL)", max_length=120, unique=True, db_index=True)
    title = models.CharField("Название", max_length=512)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="tours",
        verbose_name="Регион",
    )
    country = models.CharField("Страна", max_length=120, default="Россия")
    activity_type = models.CharField("Тип активности (текст)", max_length=200)
    activity_kind = models.CharField(
        "Вид активности (код)",
        max_length=32,
        help_text="hike, kayak, horse, mountain",
    )
    difficulty = models.CharField(
        "Сложность (код)",
        max_length=20,
        help_text="easy, medium, hard, very_hard",
    )
    difficulty_score = models.PositiveSmallIntegerField("Оценка сложности", default=1)
    difficulty_max = models.PositiveSmallIntegerField("Максимум шкалы сложности", default=5)
    distance_km = models.PositiveIntegerField("Дистанция, км", default=0)
    duration_days = models.PositiveIntegerField("Длительность, дней", default=1)
    backpack_weight_kg = models.PositiveIntegerField("Вес рюкзака, кг", default=0)
    max_people = models.PositiveIntegerField("Максимум человек в группе", default=20)
    price = models.PositiveIntegerField("Цена")
    old_price = models.PositiveIntegerField("Старая цена", null=True, blank=True)
    currency = models.CharField("Валюта", max_length=8, default="RUB")
    status_label = models.CharField("Метка статуса", max_length=80, blank=True)
    spots_left = models.PositiveIntegerField("Осталось мест", null=True, blank=True)
    description = models.TextField("Описание")
    tags = models.JSONField("Теги", default=list, help_text="Список строк")
    date_slots = models.JSONField(
        "Слоты дат",
        default=list,
        help_text="id, label, start, end (ISO YYYY-MM-DD). Краткая строка дат на сайте берётся из первого слота с датами.",
    )
    season = models.ForeignKey(
        Season,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tours",
        verbose_name="Сезон",
    )
    holiday = models.JSONField("Праздники", null=True, blank=True, default=list)
    duration_category = models.ForeignKey(
        DurationCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tours",
        verbose_name="Категория длительности",
    )
    first_start = models.DateField(
        "Первая дата выезда",
        null=True,
        blank=True,
        db_index=True,
        help_text="Заполняется из date_slots при сохранении (сортировка каталога в БД).",
    )

    #: Сколько кадров в превью на странице тура: одно главное + четыре миниатюры.
    GALLERY_PREVIEW_MAX = 5

    class Meta:
        ordering = ["id"]
        verbose_name = "Тур"
        verbose_name_plural = "Туры"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        self.first_start = first_start_date_from_slots(self.date_slots)
        super().save(*args, **kwargs)
        TourDateSlot.objects.filter(tour_id=self.pk).delete()
        rows: list[TourDateSlot] = []
        for pos, s in enumerate(self.date_slots or []):
            sd = ed = None
            if s.get("start"):
                try:
                    sd = date.fromisoformat(str(s["start"])[:10])
                except ValueError:
                    pass
            if s.get("end"):
                try:
                    ed = date.fromisoformat(str(s["end"])[:10])
                except ValueError:
                    pass
            rows.append(
                TourDateSlot(
                    tour=self,
                    position=pos,
                    slot_key=str(s.get("id") or "")[:64],
                    label=str(s.get("label") or "")[:200],
                    start=sd,
                    end=ed,
                )
            )
        if rows:
            TourDateSlot.objects.bulk_create(rows)

    @property
    def date_summary(self) -> str:
        """Текст для карточки и сайта: из первого слота `date_slots` (start/end ISO)."""
        return date_summary_from_slots(self.date_slots)

    @property
    def gallery_extra_photos_count(self) -> int:
        """Снимков сверх превью (1 главное + 4 миниатюры) — для подписи «+N» в галерее."""
        cache = getattr(self, "_prefetched_objects_cache", None)
        if cache is not None and "gallery_images" in cache:
            n = len(cache["gallery_images"])
        else:
            n = self.gallery_images.count()
        return max(0, n - self.GALLERY_PREVIEW_MAX)


class TourDateSlot(models.Model):
    """Нормализованные интервалы дат тура (синхронизируются из JSON date_slots при сохранении тура)."""

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="date_slot_rows",
        verbose_name="Тур",
    )
    position = models.PositiveSmallIntegerField("Порядок", default=0)
    slot_key = models.CharField("id слота", max_length=64, blank=True)
    label = models.CharField("Подпись", max_length=200, blank=True)
    start = models.DateField("Начало", null=True, blank=True)
    end = models.DateField("Конец", null=True, blank=True)

    class Meta:
        ordering = ["position", "id"]
        verbose_name = "Слот даты"
        verbose_name_plural = "Слоты дат"

    def __str__(self) -> str:
        return f"{self.tour_id}: {self.start}–{self.end}"


class Instructor(models.Model):
    """Инструктор (может быть привязан к нескольким турам через TourInstructor)."""

    key = models.SlugField("Ключ", max_length=64, unique=True, help_text="Стабильный id, например из сидов")
    name = models.CharField("Имя", max_length=200)
    avatar_url = models.URLField("Фото URL", max_length=512, blank=True)

    class Meta:
        ordering = ["name", "key"]
        verbose_name = "Инструктор"
        verbose_name_plural = "Инструкторы"

    def __str__(self) -> str:
        return self.name


class TourInstructor(models.Model):
    """Состав инструкторов тура (порядок отображения — поле order)."""

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="instructor_links",
        verbose_name="Тур",
    )
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        related_name="tour_links",
        verbose_name="Инструктор",
    )
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Инструктор в туре"
        verbose_name_plural = "Инструкторы тура"
        constraints = [
            models.UniqueConstraint(
                fields=["tour", "instructor"],
                name="tours_tourinstructor_unique_tour_instructor",
            )
        ]

    def __str__(self) -> str:
        return f"{self.tour_id}: {self.instructor}"


class TourProgramDay(models.Model):
    """День программы тура."""

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="program_days",
        verbose_name="Тур",
    )
    day_number = models.PositiveSmallIntegerField("Номер дня", default=1)
    title = models.CharField("Заголовок", max_length=300)
    body = models.TextField("Описание", blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "День программы"
        verbose_name_plural = "Программа по дням"

    def __str__(self) -> str:
        return f"День {self.day_number}: {self.title}"


class TourIncludedItem(models.Model):
    """Пункт «включено в стоимость»."""

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="included_items",
        verbose_name="Тур",
    )
    text = models.CharField("Текст", max_length=500)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Включено в стоимость"
        verbose_name_plural = "Включено в стоимость"

    def __str__(self) -> str:
        return self.text[:60]


class TourExcludedItem(models.Model):
    """Пункт «не включено»."""

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="excluded_items",
        verbose_name="Тур",
    )
    text = models.CharField("Текст", max_length=500)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Не включено"
        verbose_name_plural = "Не включено"

    def __str__(self) -> str:
        return self.text[:60]


class TourPackingItem(models.Model):
    """Пункт списка вещей."""

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="packing_items",
        verbose_name="Тур",
    )
    text = models.CharField("Текст", max_length=500)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Список вещей"
        verbose_name_plural = "Список вещей"

    def __str__(self) -> str:
        return self.text[:60]


class TourFaqItem(models.Model):
    """Вопрос и ответ по туру."""

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="faq_items",
        verbose_name="Тур",
    )
    question = models.CharField("Вопрос", max_length=400)
    answer = models.TextField("Ответ", blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Вопрос и ответ"
        verbose_name_plural = "Вопросы и ответы"

    def __str__(self) -> str:
        return self.question[:60]


class TourGalleryImage(models.Model):
    """Ссылка на изображение в галерее тура (порядок на карточке)."""

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="gallery_images",
        verbose_name="Тур",
    )
    url = models.URLField("URL изображения", max_length=512)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галереи"

    def __str__(self) -> str:
        return self.url[:48] + ("…" if len(self.url) > 48 else "")
