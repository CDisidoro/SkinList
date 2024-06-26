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
        possible_sources = {
            "FirstWin": "First victory of the season",
            "BattlePass.Free": "Free from the Battle Pass", 
            "BattlePass.Paid": "Paid from the Battle Pass", 
            "Cosmetics.LimitedTimeReward": "Limited time reward",
            "Source.ItemShop": "In game shop",
            "Source.CrewPack": "Monthly Crew Pack",
            "Source.DefaultItem": "Default item",
            "Source.Event": "Event",
            "Source.Platform": "Platform Bundle",
            "Source.Promo": "Special Promotion",
            "BattlePass.Paid.Additional": "Paid from the additional levels of the Battle Pass",
        }
        logger.warning("Fetching all cosmetics...")
        cosmetics = API.cosmetics.fetch_all()
        logger.warning("Updating cosmetic list")
        for cosmetic in cosmetics:
            if cosmetic.icon is None:
                if cosmetic.featured is None:
                    icon = cosmetic.small_icon.url
                else:
                    icon = cosmetic.featured.url
            else:
                icon = cosmetic.icon.url
            tags = cosmetic.gameplay_tags
            obtainable = "Unknown"
            if tags is not None:
                for tag in tags:
                    tagSplitted = tag.split(".")
                    if tagSplitted[-1] in possible_sources:
                        obtainable = possible_sources[tagSplitted[-1]]
                        break
                    elif tagSplitted[-2] + "." + tagSplitted[-1] in possible_sources:
                        obtainable = possible_sources[tagSplitted[-2] + "." + tagSplitted[-1]]
                        break
                    elif len(tagSplitted) >= 3 and tagSplitted[-3] + "." + tagSplitted[-2] + "." + tagSplitted[-1] in possible_sources:
                        obtainable = possible_sources[tagSplitted[-3] + "." + tagSplitted[-2] + "." + tagSplitted[-1]]
                        break
            Cosmetic.objects.update_or_create(
                id=cosmetic.id,
                defaults={
                    'name': cosmetic.name,
                    'description': cosmetic.description,
                    'type': cosmetic.display_type,
                    'rarity': cosmetic.rarity_text,
                    'introduction': cosmetic.added,
                    'icon': icon,
                    'obtainable': obtainable
                }
            )
        logger.warning("Cosmetic list updated")