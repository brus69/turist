from django.core.management.base import BaseCommand

from tours.models import Tour
from tours.seed_data import SEED_TOURS


class Command(BaseCommand):
    help = "Заполнить базу турами (идемпотентно по slug)."

    def handle(self, *args, **options):
        for row in SEED_TOURS:
            slug = row["slug"]
            Tour.objects.update_or_create(slug=slug, defaults=row)
        self.stdout.write(self.style.SUCCESS(f"OK: {len(SEED_TOURS)} туров"))
