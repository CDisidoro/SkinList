from django.core.management.base import BaseCommand
from ...models import Cosmetic
import logging
import fortnite_api
import os

class Command(BaseCommand):
    help = 'Updates the cosmetics'

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        API = fortnite_api.FortniteAPI(os.getenv('FORT_SECRET'))

        logger.warning("Fetching all cosmetics...")
        cosmetics = API.cosmetics.fetch_all()
        logger.warning("Updating cosmetic list")
        for cosmetic in cosmetics:
            Cosmetic.objects.update_or_create(
                id=cosmetic.id,
                defaults={
                    'name': cosmetic.name,
                    'description': cosmetic.description,
                    'type': cosmetic.display_type,
                    'rarity': cosmetic.rarity_text,
                    'introduction': cosmetic.added,
                    # 'icon': cosmetic.images.icon
                }
            )
        logger.warning("Cosmetic list updated")