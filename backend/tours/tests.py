from datetime import date

from django.test import SimpleTestCase, TestCase

from .breadcrumbs import tour_breadcrumb_links
from .filters import filter_tours
from .models import DurationCategory, Season, Tour, TourDateSlot, date_summary_from_slots, first_start_date_from_slots


def _minimal_tour_kwargs(slug: str, **extra):
    base = {
        "slug": slug,
        "title": "Тестовый тур",
        "region": "Тестовый регион",
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


class TourBreadcrumbLinksTests(SimpleTestCase):
    def test_links_home_country_region(self):
        t = Tour(
            slug="x",
            title="T",
            region="Карелия и Ленобласть",
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
        t = Tour(
            slug="x",
            title="T",
            region="Россия",
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
