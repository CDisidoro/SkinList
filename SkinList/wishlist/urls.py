from django.urls import path
from . import views

urlpatterns = [
    path("", views.shop, name="index"),
    path("shop", views.shop, name="shop"),
    path("cosmetics", views.cosmetics, name="cosmetics"),
    path("bundles", views.bundles, name="bundles"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("login", views.getlogin, name="login"),
    path("postLogin", views.postLogin, name="postLogin"),
    path("logout", views.postLogout, name="logout"),
    path("register", views.register, name="register"),
    path("postRegister", views.postRegister, name="postRegister"),
    path("cosmetic/<cosmetic_id>", views.cosmetic, name="cosmetic"),
    path("wishlistAdd/<cosmetic_id>", views.wishlistAdd, name="wishlistAdd"),
    path("wishlistRemove/<cosmetic_id>", views.wishlistRemove, name="wishlistRemove"),
]