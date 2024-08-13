from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from SkinList import settings
from .models import ShopItem, Cosmetic, Bundle, Wishlist
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
    searchQuery = request.GET.get('searchQuery')
    logger.info("Search query: " + str(searchQuery))
    if searchQuery:
        cosmeticsInShop = ShopItem.objects.filter(shop=latest_shop.shop, cosmetic__name__icontains=searchQuery)
    else:
        cosmeticsInShop = ShopItem.objects.filter(shop=latest_shop.shop)
    logger.info("cosmetics in shop: " + str(cosmeticsInShop))
    itemsInShop = [item.cosmetic for item in cosmeticsInShop]
    context = {
        'itemsInShop': itemsInShop,
        'shopDate': latest_shop.shop.date
    }
    return render(request, 'wishlist/shop.html', context)

def cosmetics(request):
    searchQuery = request.GET.get('searchQuery')
    logger.info("Search query: " + str(searchQuery))
    if searchQuery:
        cosmetics = Cosmetic.objects.filter(name__icontains=searchQuery)
    else:
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
    if request.user.is_authenticated:
        userID = request.user.id
        userWishlist = Wishlist.objects.filter(user=userID, cosmetic=cosmetic_id)
        logger.info("User wishlist: " + str(userWishlist))
        logger.info("Item in wishlist?: " + str(len(userWishlist) > 0))
        context['inWishList'] = len(userWishlist)
    return render(request, 'wishlist/cosmetic.html', context)

def bundles(request):
    searchQuery = request.GET.get('searchQuery')
    logger.info("Search query: " + str(searchQuery))
    if searchQuery:
        bundles = Bundle.objects.filter(name__icontains=searchQuery)
    else:
        bundles = Bundle.objects.all()
    context = {
        'bundles': bundles
    }
    return render(request, 'wishlist/bundles.html', context)

def wishlist(request):
    if request.user.is_authenticated:
        userWishlist = Wishlist.objects.filter(user=request.user.id)
        logger.info("User wishlist: " + str(userWishlist))
        itemsInWishList = Cosmetic.objects.filter(id__in=[item.cosmetic_id for item in userWishlist])
        logger.info("Items in wishlist: " + str(itemsInWishList))
        context = {
            'wishList': itemsInWishList
        }
        return render(request, 'wishlist/wishlist.html', context)
    else:
        messages.info(request, 'You need to be logged in to view your wishlist')
        return redirect("login")

def wishlistRemove(request, cosmetic_id):
    if request.user.is_authenticated:
        userID = request.user.id
        userWishlist = Wishlist.objects.filter(user=userID, cosmetic=cosmetic_id)
        userWishlist.delete()
        return redirect('wishlist')
    else:
        messages.warning(request, 'You need to be logged in to remove items from your wishlist')
        return redirect('login')
    
def wishlistAdd(request, cosmetic_id):
    if request.user.is_authenticated:
        userID = request.user.id
        Wishlist.objects.update_or_create(
            user_id=userID,
            cosmetic_id=cosmetic_id
        )
        return redirect('wishlist')
    else:
        messages.warning(request, 'You need to be logged in to add items to your wishlist')
        return redirect('login')

def getlogin(request):
    return render(request, 'wishlist/login.html')

def postLogin(request):
    missingFields = 0
    username = request.POST['username']
    if not username:
        missingFields += 1
    password = request.POST['password']
    if not password:
        missingFields += 1
    logger.warning("Login Missing fields: " + str(missingFields))
    user = authenticate(request, username=username, password=password)
    if user is not None and missingFields == 0:
        login(request, user)
        messages.success(request, 'You have successfully logged in')
        return redirect('index')
    else:
        messages.error(request, 'Invalid credentials')
        return redirect('login')

def register(request):
    return render(request, 'wishlist/register.html')

def postRegister(request):
    missingFields = 0
    username = request.POST['username']
    if not username:
        missingFields += 1
    password = request.POST['password']
    if not password:
        missingFields += 1
    email = request.POST['email']
    if not email:
        missingFields += 1
    first_name = request.POST['first_name']
    if not first_name:
        missingFields += 1
    last_name = request.POST['last_name']
    if not last_name:
        missingFields += 1
    logger.warning("Register Missing fields: " + str(missingFields))
    if missingFields > 0:
        messages.error(request, 'Please fill in all fields')
        return redirect('register')
    user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
    user.save()
    authedUser = authenticate(request, username=username, password=password)
    login(request, authedUser)
    messages.success(request, 'You have successfully registered')
    return redirect('index')

def postLogout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('index')