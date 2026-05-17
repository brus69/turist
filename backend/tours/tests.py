from datetime import date

from django.template import Context, Template
from django.test import RequestFactory, TestCase

from .breadcrumbs import tour_breadcrumb_links
from .catalog_params import catalog_params_from_request, merge_query_pairs
from .filters import filter_tours
from .search import search_instructors, search_tours
from .models import (
    DurationCategory,
    Instructor,
    Region,
    Season,
    Tag,
    Tour,
    TourDateSlot,
    date_summary_from_slots,
    first_start_date_from_slots,
    normalize_date_slots_for_save,
)


def _minimal_tour_kwargs(slug: str, **extra):
    reg, _ = Region.objects.get_or_create(name="Тестовый регион", defaults={"order": 900})
    base = {
        "slug": slug,
        "title": "Тестовый тур",
        "region": reg,
        "country": "Россия",
        "activity_type": "Пешие походы",
        "activity_kind": "hike",
        "difficulty": "easy",
        "price": 10000,
        "description": "Описание для теста.",
        "date_slots": [
            {"id": "a", "label": "1–2 июня", "start": "2026-06-01", "end": "2026-06-02"},
        ],
    }
    base.update(extra)
    return base


class TourBreadcrumbLinksTests(TestCase):
    def test_links_home_country_region(self):
        r, _ = Region.objects.get_or_create(name="Карелия и Ленобласть", defaults={"order": 1})
        t = Tour(
            slug="x",
            title="T",
            region=r,
            country="Россия",
            activity_type="Пешие",
            activity_kind="hike",
            difficulty="easy",
            price=1,
            description="d",
        )
        links = tour_breadcrumb_links(t)
        labels = [x["label"] for x in links]
        self.assertEqual(labels[0], "Главная")
        self.assertIn("Россия", labels)
        self.assertIn("Карелия и Ленобласть", labels)

    def test_same_region_as_country_skips_duplicate(self):
        r, _ = Region.objects.get_or_create(name="Россия", defaults={"order": 0})
        t = Tour(
            slug="x",
            title="T",
            region=r,
            country="Россия",
            activity_type="Пешие",
            activity_kind="hike",
            difficulty="easy",
            price=1,
            description="d",
        )
        links = tour_breadcrumb_links(t)
        self.assertEqual([x["label"] for x in links], ["Главная", "Россия"])


class UrlSmokeTests(TestCase):
    def setUp(self):
        Tour.objects.create(**_minimal_tour_kwargs("smoke-tour"))

    def test_home(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)

    def test_catalog(self):
        r = self.client.get("/tours/")
        self.assertEqual(r.status_code, 200)

    def test_tour_detail(self):
        r = self.client.get("/tours/smoke-tour/")
        self.assertEqual(r.status_code, 200)

    def test_site_search_page(self):
        r = self.client.get("/search/")
        self.assertEqual(r.status_code, 200)

    def test_site_search_finds_tour(self):
        r = self.client.get("/search/", {"q": "Тестовый"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "smoke-tour")
        self.assertContains(r, "Туры")


class InstructorPagesTests(TestCase):
    def setUp(self):
        Instructor.objects.create(
            key="test-i",
            slug="test-instructor",
            name="Тест Инструктор",
            description="Описание для персональной страницы.",
        )

    def test_instructor_list(self):
        r = self.client.get("/instructors/")
        self.assertEqual(r.status_code, 200)

    def test_instructor_detail(self):
        r = self.client.get("/instructors/test-instructor/")
        self.assertEqual(r.status_code, 200)


class NormalizeDateSlotsTests(TestCase):
    def test_normalize_strips_id_and_sets_label(self):
        raw = [
            {"id": "custom", "label": "ручная", "start": "2026-05-08", "end": "2026-05-10"},
            {"start": "2026-07-01", "end": "2026-07-05"},
        ]
        out = normalize_date_slots_for_save(raw)
        self.assertNotIn("id", out[0])
        self.assertEqual(set(out[0].keys()), {"start", "end", "label"})
        self.assertIn("мая", out[0]["label"])
        self.assertNotEqual(out[0]["label"], "ручная")

    def test_save_tour_normalizes_date_slots(self):
        reg, _ = Region.objects.get_or_create(name="Регион X", defaults={"order": 1})
        t = Tour.objects.create(
            slug="norm-slots",
            title="N",
            region=reg,
            activity_type="Пешие",
            activity_kind="hike",
            difficulty="easy",
            price=100,
            description="d",
            date_slots=[{"id": "z", "label": "x", "start": "2026-06-01", "end": "2026-06-02"}],
        )
        t.refresh_from_db()
        self.assertNotIn("id", t.date_slots[0])
        self.assertIn("июня", t.date_slots[0]["label"])


class DateSummaryAndSlotsTests(TestCase):
    def test_date_summary_from_slots(self):
        s = date_summary_from_slots(
            [{"id": "x", "label": "май", "start": "2026-05-08", "end": "2026-05-10"}]
        )
        self.assertIn("2026", s or "")
        self.assertIn("мая", s)

    def test_first_start_and_slot_rows_on_save(self):
        t = Tour.objects.create(**_minimal_tour_kwargs("slot-sync"))
        self.assertEqual(t.first_start, date(2026, 6, 1))
        rows = list(TourDateSlot.objects.filter(tour=t))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].start, date(2026, 6, 1))
        self.assertEqual(rows[0].end, date(2026, 6, 2))


class FilterToursOrmTests(TestCase):
    def setUp(self):
        summer, _ = Season.objects.get_or_create(code="summer", defaults={"name": "Лето", "order": 1})
        weekend, _ = DurationCategory.objects.get_or_create(
            code="weekend", defaults={"name": "На выходные", "order": 2}
        )
        ta = Tour.objects.create(**_minimal_tour_kwargs("f-a", title="Альпы поход", price=5000))
        tb = Tour.objects.create(
            **_minimal_tour_kwargs(
                "f-b",
                title="Другой тур",
                price=15000,
                date_slots=[
                    {"id": "1", "label": "июль", "start": "2026-07-01", "end": "2026-07-05"},
                ],
            )
        )
        tb.season = summer
        tb.save(update_fields=["season"])
        tb.duration_category = weekend
        tb.save(update_fields=["duration_category"])

    def test_filter_price_and_q(self):
        out = filter_tours(Tour.objects.all(), {"q": "Альпы", "price_max": "8000"})
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].slug, "f-a")

    def test_filter_when_range(self):
        out = filter_tours(Tour.objects.all(), {"from": "2026-06-15", "to": "2026-06-20"})
        self.assertEqual(len(out), 0)
        out2 = filter_tours(Tour.objects.all(), {"from": "2026-06-01", "to": "2026-06-02"})
        self.assertEqual({t.slug for t in out2}, {"f-a"})

    def test_filter_season(self):
        out = filter_tours(Tour.objects.all(), {"season": "summer"})
        self.assertEqual({t.slug for t in out}, {"f-b"})

    def test_filter_duration(self):
        out = filter_tours(Tour.objects.all(), {"duration": "weekend"})
        self.assertEqual({t.slug for t in out}, {"f-b"})

    def test_filter_region_by_name(self):
        out = filter_tours(Tour.objects.all(), {"region": "Тестовый регион"})
        self.assertEqual({t.slug for t in out}, {"f-a", "f-b"})

    def test_filter_difficulty(self):
        ta = Tour.objects.get(slug="f-a")
        tb = Tour.objects.get(slug="f-b")
        ta.difficulty = "easy"
        tb.difficulty = "hard"
        ta.save(update_fields=["difficulty"])
        tb.save(update_fields=["difficulty"])
        out = filter_tours(Tour.objects.all(), {"difficulty": "easy"})
        self.assertEqual({t.slug for t in out}, {"f-a"})

    def test_filter_holiday(self):
        tb = Tour.objects.get(slug="f-b")
        tb.holiday = ["may"]
        tb.save(update_fields=["holiday"])
        out = filter_tours(Tour.objects.all(), {"holiday": "may"})
        self.assertEqual({t.slug for t in out}, {"f-b"})

    def test_filter_activity(self):
        ta = Tour.objects.get(slug="f-a")
        ta.activity_kind = "kayak"
        ta.save(update_fields=["activity_kind"])
        out = filter_tours(Tour.objects.all(), {"activity": "kayak"})
        self.assertEqual({t.slug for t in out}, {"f-a"})

    def test_filter_multi_season_or(self):
        winter, _ = Season.objects.get_or_create(code="winter", defaults={"name": "Зима", "order": 2})
        ta = Tour.objects.get(slug="f-a")
        ta.season = winter
        ta.save(update_fields=["season"])
        out = filter_tours(Tour.objects.all(), {"season": "summer,winter"})
        self.assertEqual({t.slug for t in out}, {"f-a", "f-b"})

    def test_filter_combo(self):
        ta = Tour.objects.get(slug="f-a")
        tb = Tour.objects.get(slug="f-b")
        ta.difficulty = "easy"
        tb.difficulty = "hard"
        ta.save(update_fields=["difficulty"])
        tb.save(update_fields=["difficulty"])
        out = filter_tours(
            Tour.objects.all(),
            {"region": "Тестовый регион", "priceMin": "4000", "difficulty": "easy"},
        )
        self.assertEqual({t.slug for t in out}, {"f-a"})

    def test_filter_q_by_description(self):
        ta = Tour.objects.get(slug="f-a")
        ta.description = "УникальноеСловоВОписании"
        ta.save(update_fields=["description"])
        out = filter_tours(Tour.objects.all(), {"q": "УникальноеСлово"})
        self.assertEqual({t.slug for t in out}, {"f-a"})

    def test_filter_ignores_invalid_codes(self):
        out = filter_tours(
            Tour.objects.all(),
            {"activity": "invalid", "holiday": "bogus", "difficulty": "impossible"},
        )
        self.assertEqual({t.slug for t in out}, {"f-a", "f-b"})


class TourTagTests(TestCase):
    def setUp(self):
        reg, _ = Region.objects.get_or_create(name="Регион тегов", defaults={"order": 900})
        self.tag_a, _ = Tag.objects.get_or_create(name="Пешие походы")
        self.tag_b, _ = Tag.objects.get_or_create(name="На выходные")
        self.tour = Tour.objects.create(**_minimal_tour_kwargs("tagged-tour", region=reg))
        self.tour.tags.set([self.tag_a, self.tag_b])
        Tour.objects.create(**_minimal_tour_kwargs("other-tour", region=reg, title="Другой тур"))

    def test_tour_tags_m2m(self):
        names = list(self.tour.tags.values_list("name", flat=True))
        self.assertEqual(sorted(names), ["На выходные", "Пешие походы"])

    def test_filter_by_tag(self):
        out = filter_tours(Tour.objects.all(), {"tag": "Пешие походы"})
        self.assertEqual({t.slug for t in out}, {"tagged-tour"})

    def test_filter_tag_distinct(self):
        out = filter_tours(Tour.objects.all(), {"tag": "Пешие походы"})
        self.assertEqual(len(out), 1)

    def test_catalog_filter_by_tag_url(self):
        r = self.client.get("/tours/", {"tag": "На выходные"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "tagged-tour")
        self.assertNotContains(r, "other-tour")
        self.assertContains(r, "?tag=")


class SiteSearchTests(TestCase):
    def setUp(self):
        Tour.objects.create(**_minimal_tour_kwargs("search-tour", title="Поход в Карелию"))
        Instructor.objects.create(
            key="search-i",
            slug="karelia-guide",
            name="Гид Карелии",
            description="Проводник по северным маршрутам.",
        )

    def test_search_tours_by_title(self):
        out = search_tours(Tour.objects.all(), "Карелию")
        self.assertEqual([t.slug for t in out], ["search-tour"])

    def test_search_instructors_by_name(self):
        out = search_instructors(Instructor.objects.all(), "Карелии")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].slug, "karelia-guide")

    def test_search_page_shows_instructor(self):
        r = self.client.get("/search/", {"q": "Карелии"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "karelia-guide")
        self.assertContains(r, "Инструкторы")


class CatalogFilterHttpTests(TestCase):
    def setUp(self):
        summer, _ = Season.objects.get_or_create(code="summer", defaults={"name": "Лето", "order": 1})
        self.assertTrue(summer)
        weekend, _ = DurationCategory.objects.get_or_create(
            code="weekend", defaults={"name": "На выходные", "order": 2}
        )
        self.assertTrue(weekend)
        tb = Tour.objects.create(
            **_minimal_tour_kwargs(
                "http-b",
                title="Каталог HTTP",
                date_slots=[
                    {"start": "2026-07-01", "end": "2026-07-05"},
                ],
            )
        )
        tb.season = summer
        tb.duration_category = weekend
        tb.holiday = ["may"]
        tb.activity_kind = "hike"
        tb.save(update_fields=["season", "duration_category", "holiday", "activity_kind"])
        Tour.objects.create(**_minimal_tour_kwargs("http-other", title="Другой"))

    def test_catalog_duration_and_season(self):
        r = self.client.get("/tours/", {"duration": "weekend", "season": "summer"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "http-b")
        self.assertNotContains(r, "http-other")

    def test_catalog_activity(self):
        r = self.client.get("/tours/", {"activity": "hike"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "http-b")

    def test_catalog_sort_preserves_multi_filters(self):
        r = self.client.get(
            "/tours/",
            [
                ("duration", "weekend"),
                ("season", "summer"),
                ("sort", "price"),
                ("dir", "asc"),
            ],
        )
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'name="season" value="summer" checked')
        self.assertContains(r, 'name="duration" value="weekend" checked')


class QueryUpdateTagTests(TestCase):
    def setUp(self):
        Season.objects.get_or_create(code="summer", defaults={"name": "Лето", "order": 1})
        Season.objects.get_or_create(code="winter", defaults={"name": "Зима", "order": 2})
        DurationCategory.objects.get_or_create(code="weekend", defaults={"name": "На выходные", "order": 2})

    def test_query_update_preserves_multi_season(self):
        request = RequestFactory().get(
            "/tours/",
            [("season", "summer"), ("season", "winter"), ("duration", "weekend")],
        )
        duration_codes = frozenset(DurationCategory.objects.values_list("code", flat=True))
        season_codes = frozenset(Season.objects.values_list("code", flat=True))
        params = catalog_params_from_request(
            request,
            duration_codes=duration_codes,
            season_codes=season_codes,
        )
        qs = merge_query_pairs(params.query_pairs(), sort="price", dir="asc")
        self.assertIn("season=summer", qs)
        self.assertIn("season=winter", qs)
        self.assertIn("duration=weekend", qs)
        self.assertIn("sort=price", qs)

    def test_query_update_template_tag(self):
        request = RequestFactory().get(
            "/tours/",
            [("season", "summer"), ("season", "winter")],
        )
        tpl = Template("{% load catalog_tags %}{% query_update sort='price' dir='asc' %}")
        out = tpl.render(Context({"request": request}))
        self.assertIn("season=summer", out)
        self.assertIn("season=winter", out)
        self.assertIn("sort=price", out)
