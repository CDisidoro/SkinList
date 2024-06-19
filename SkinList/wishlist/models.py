from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.TextField()
    def __str__(self):
        return "ID: "+ str(self.id) + "; Username: " + self.username + "; Email: " + self.email

class Cosmetic(models.Model):
    id = models.CharField(max_length=191, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(max_length=50)
    rarity = models.CharField(max_length=50)
    introduction = models.DateTimeField()
    #icon = models.FilePathField(path="/img")

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE)

class Shop(models.Model):
    hash = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField()

class ShopItems(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField()

class Bundle(models.Model):
    id = models.CharField(max_length=190, primary_key=True)
    name = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField()
    cosmetics = models.ManyToManyField(Cosmetic)