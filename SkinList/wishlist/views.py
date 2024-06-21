from django.shortcuts import render
from .models import ShopItem, Cosmetic, Bundle
import fortnite_api
import logging
import os
# Create your views here.
API = fortnite_api.FortniteAPI(os.getenv('FORT_SECRET'))
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'wishlist/index.html', {})

def shop(request):
    latest_shop = ShopItem.objects.latest('shop__date')
    logger.info("latest shop: " + str(latest_shop.shop.date))
    cosmeticsInShop = ShopItem.objects.filter(shop=latest_shop.shop)
    logger.info("cosmetics in shop: " + str(cosmeticsInShop))
    itemsInShop = [item.cosmetic for item in cosmeticsInShop]
    context = {
        'itemsInShop': itemsInShop
    }
    return render(request, 'wishlist/shop.html', context)

def cosmetics(request):
    cosmetics = Cosmetic.objects.all()
    context = {
        'cosmetics': cosmetics
    }
    return render(request, 'wishlist/cosmetics.html', context)

def bundles(request):
    bundles = Bundle.objects.all()
    context = {
        'bundles': bundles
    }
    return render(request, 'wishlist/bundles.html', context)