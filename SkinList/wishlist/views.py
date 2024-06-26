from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from SkinList import settings
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
        'itemsInShop': itemsInShop,
        'shopDate': latest_shop.shop.date,
    }
    return render(request, 'wishlist/shop.html', context)

def cosmetics(request):
    cosmetics = Cosmetic.objects.all()
    context = {
        'cosmetics': cosmetics
    }
    return render(request, 'wishlist/cosmetics.html', context)

def cosmetic(request, cosmetic_id):
    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)
    context = {
        'cosmetic': cosmetic
    }
    return render(request, 'wishlist/cosmetic.html', context)

def bundles(request):
    bundles = Bundle.objects.all()
    context = {
        'bundles': bundles
    }
    return render(request, 'wishlist/bundles.html', context)

def wishlist(request):
    if request.user.is_authenticated:
        return render(request, 'wishlist/wishlist.html')
    else:
        return redirect("login")

def getlogin(request):
    return render(request, 'wishlist/login.html')

def postLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('wishlist')
    else:
        return redirect('login')

def register(request):
    return render(request, 'wishlist/register.html')

def postRegister(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
    user.save()
    return redirect('index')

def postLogout(request):
    logout(request)
    return redirect('index')