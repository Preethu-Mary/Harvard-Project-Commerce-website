from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bidValue = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="bidder")

    def __str__(self) -> str:
        return str(self.bidValue)

class Category(models.Model):
    Category = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.Category

class Listing(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=500)
    imageUrl = models.CharField(max_length=2000)
    startingPrice = models.FloatField(default=0)
    currentPrice = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null= True, related_name="bid")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null= True, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="user")
    isActive = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlistitems")

    def __str__(self) -> str:
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name="commenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True,related_name="listing")
    message = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return f"{self.user} commented on {self.listing}"
    
