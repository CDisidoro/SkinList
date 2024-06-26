from django.db import models
from django.conf import settings

# Create your models here.

class Cosmetic(models.Model):
    id = models.CharField(max_length=191, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(max_length=50)
    rarity = models.CharField(max_length=50)
    introduction = models.DateTimeField()
    icon = models.TextField()
    obtainable = models.TextField()
    def __str__(self):
        return "ID: "+ str(self.id) + "; Name: " + self.name + "; Obtainable: " + self.obtainable

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE)
    def __str__(self):
        return "User: "+ str(self.user) + "; Cosmetic: " + str(self.cosmetic)

class Shop(models.Model):
    hash = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField()
    def __str__(self):
        return "Hash: "+ self.hash + "; Date: " + str(self.date)

class ShopItem(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField()
    def __str__(self):
        return "Shop: "+ str(self.shop) + "; Cosmetic: " + str(self.cosmetic) + "; Price: " + str(self.price)

class Bundle(models.Model):
    id = models.CharField(max_length=190, primary_key=True)
    name = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField()
    cosmetics = models.ManyToManyField(Cosmetic)
    def __str__(self):
        return "ID: "+ str(self.id) + "; Name: " + self.name + "; Price: " + str(self.price) + "; Cosmetics: " + str(self.cosmetics)