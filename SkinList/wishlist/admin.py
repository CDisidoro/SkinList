from django.contrib import admin

# Register your models here.
from .models import User, Cosmetic, Wishlist, Shop, ShopItem, Bundle

admin.site.register(User)
admin.site.register(Cosmetic)
admin.site.register(Wishlist)
admin.site.register(Shop)
admin.site.register(ShopItem)
admin.site.register(Bundle)
