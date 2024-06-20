from django.shortcuts import render
from django.http import HttpResponse
import fortnite_api
from fortnite_api import shop
# Create your views here.
API = fortnite_api.FortniteAPI("20e3d446-6d3e-434c-9da8-29f4b7ba43f6")
def index(request):
    print("Fetching shop...")
    shop = API.shop.fetch()
    featuredEntries = shop.featured.entries
    itemsInShop = []
    for entry in featuredEntries:
        entryItems = entry.items
        itemsInShop.extend(entryItems)
    return HttpResponse(itemsInShop)