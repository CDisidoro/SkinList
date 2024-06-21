from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import fortnite_api
import logging
from fortnite_api import shop
# Create your views here.
API = fortnite_api.FortniteAPI("20e3d446-6d3e-434c-9da8-29f4b7ba43f6")
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'wishlist/index.html', {})

def shop(request):
    logger.info("Fetching shop...")
    shop = API.shop.fetch()
    featuredEntries = shop.featured.entries
    itemsInShop = []
    for entry in featuredEntries:
        entryItems = entry.items
        itemsInShop.extend(entryItems)
    context = {
        'itemsInShop': itemsInShop
    }
    return render(request, 'wishlist/shop.html', context)