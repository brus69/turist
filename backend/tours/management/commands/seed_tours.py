from django.core.management.base import BaseCommand

from tours.models import (
    DurationCategory,
    Instructor,
    Season,
    Tour,
    TourExcludedItem,
    TourFaqItem,
    TourGalleryImage,
    TourIncludedItem,
    TourInstructor,
    TourPackingItem,
    TourProgramDay,
)
from tours.seed_data import SEED_TOURS

_SEED_SKIP_KEYS = frozenset(
    {
        "slug",
        "season",
        "duration_category",
        "instructors",
        "program_by_day",
        "included",
        "not_included",
        "packing_list",
        "faq",
        "images",
    }
)
_SEED_ALLOWED_KEYS = frozenset(f.name for f in Tour._meta.fields if f.name != "id")


def _sync_tour_lists_from_row(tour: Tour, row: dict) -> None:
    program = row.get("program_by_day")
    if not isinstance(program, list):
        program = []
    TourProgramDay.objects.filter(tour=tour).delete()
    for idx, d in enumerate(program):
        if not isinstance(d, dict):
            continue
        try:
            dn = int(d.get("day") or idx + 1)
        except (TypeError, ValueError):
            dn = idx + 1
        title = str(d.get("title") or "")[:300]
        body = str(d.get("body") or "")
        if not title.strip() and not body.strip():
            continue
        TourProgramDay.objects.create(
            tour=tour,
            day_number=max(1, min(dn, 32767)),
            title=title or f"День {dn}",
            body=body,
            order=idx,
        )

    def _sync_lines(model, key: str) -> None:
        raw = row.get(key)
        if not isinstance(raw, list):
            raw = []
        model.objects.filter(tour=tour).delete()
        for idx, text in enumerate(raw):
            if not isinstance(text, str) or not text.strip():
                continue
            model.objects.create(tour=tour, text=text[:500], order=idx)

    _sync_lines(TourIncludedItem, "included")
    _sync_lines(TourExcludedItem, "not_included")
    _sync_lines(TourPackingItem, "packing_list")

    faq = row.get("faq")
    if not isinstance(faq, list):
        faq = []
    TourFaqItem.objects.filter(tour=tour).delete()
    for idx, item in enumerate(faq):
        if not isinstance(item, dict):
            continue
        q = str(item.get("q") or "").strip()
        a = str(item.get("a") or "")
        if not q and not a.strip():
            continue
        TourFaqItem.objects.create(tour=tour, question=(q or "Вопрос")[:400], answer=a, order=idx)


def _sync_tour_season_and_duration_from_row(tour: Tour, row: dict) -> None:
    sraw = row.get("season")
    scode = None
    if isinstance(sraw, str) and sraw.strip():
        scode = sraw.strip()
    elif isinstance(sraw, list):
        for c in sraw:
            if isinstance(c, str) and c.strip():
                scode = c.strip()
                break
    tour.season = Season.objects.filter(code=scode).first() if scode else None

    draw = row.get("duration_category")
    dcode = None
    if isinstance(draw, str) and draw.strip():
        dcode = draw.strip()
    elif isinstance(draw, list):
        for c in draw:
            if isinstance(c, str) and c.strip():
                dcode = c.strip()
                break
    tour.duration_category = DurationCategory.objects.filter(code=dcode).first() if dcode else None

    tour.save(update_fields=["season", "duration_category"])


def _sync_gallery_from_row(tour: Tour, row: dict) -> None:
    raw = row.get("images")
    if not isinstance(raw, list):
        raw = []
    TourGalleryImage.objects.filter(tour=tour).delete()
    for idx, u in enumerate(raw):
        if not isinstance(u, str) or not u.strip():
            continue
        TourGalleryImage.objects.create(tour=tour, url=u[:512], order=idx)


class Command(BaseCommand):
    help = "Заполнить базу турами (идемпотентно по slug)."

    def handle(self, *args, **options):
        for row in SEED_TOURS:
            slug = row["slug"]
            instructor_rows = row.get("instructors")
            if not isinstance(instructor_rows, list):
                instructor_rows = []
            defaults = {
                k: v
                for k, v in row.items()
                if k not in _SEED_SKIP_KEYS and k in _SEED_ALLOWED_KEYS
            }
            tour, _ = Tour.objects.update_or_create(slug=slug, defaults=defaults)
            _sync_tour_season_and_duration_from_row(tour, row)
            _sync_tour_lists_from_row(tour, row)
            _sync_gallery_from_row(tour, row)
            TourInstructor.objects.filter(tour=tour).delete()
            for idx, item in enumerate(instructor_rows):
                if not isinstance(item, dict):
                    continue
                kid = str(item.get("id") or "").strip()
                if not kid:
                    kid = f"{slug}-instr-{idx}"
                kid = kid[:64]
                name = str(item.get("name") or kid)[:200]
                av = str(item.get("avatarUrl") or "")[:512]
                inst, _ = Instructor.objects.get_or_create(key=kid, defaults={"name": name, "avatar_url": av})
                TourInstructor.objects.create(tour=tour, instructor=inst, order=idx)
        self.stdout.write(self.style.SUCCESS(f"OK: {len(SEED_TOURS)} туров"))
