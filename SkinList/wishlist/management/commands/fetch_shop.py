from django.core.management.base import BaseCommand
from ...models import Shop, Cosmetic, ShopItem, Bundle
import logging
import fortnite_api

class Command(BaseCommand):
    help = 'Updates the shop'
        
    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        API = fortnite_api.FortniteAPI("20e3d446-6d3e-434c-9da8-29f4b7ba43f6")
        logger.warning("Fetching shop...")
        shop = API.shop.fetch()
        newShop = Shop.objects.update_or_create(
            hash=shop.hash,
            date=shop.date
        )[0]
        featuredEntries = shop.featured.entries
        itemsInShop = []
        for entry in featuredEntries:
            entryItems = entry.items
            for item in entryItems:
                itemsInShop.append(item.id)
            if entry.bundle is not None:
                logger.info("Processing bundle " + entry.bundle.name)
                bundleItems = Cosmetic.objects.filter(id__in=[item.id for item in entry.items])
                bundle = Bundle.objects.update_or_create(
                    id = entry.bundle.name,
                    name = entry.bundle.name,
                    price = entry.final_price
                )[0]
                bundle.cosmetics.set(bundleItems)
        logger.warning("Updating shop items")
        logger.info("Items in shop: " + str(itemsInShop))
        activeItems = Cosmetic.objects.filter(id__in=itemsInShop)
        logger.info("Active items: " + str(activeItems))
        for item in activeItems:
            ShopItem.objects.create(
                shop=newShop,
                cosmetic=item,
                price=0
            )
        logger.warning("Shop updated")