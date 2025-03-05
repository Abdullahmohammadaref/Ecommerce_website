from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=50, blank= False, unique=True)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="publisher")
    title = models.CharField(max_length=100, blank=False)
    picture = models.URLField(blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(blank=False, decimal_places=2, max_digits=999999999)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    closed = models.BooleanField(default=False)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="listing")

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="bid_listing")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, related_name='bidder')
    bid = models.DecimalField(blank=False, decimal_places=2, max_digits=999999999)

    def __str__(self):
        return f"{self.bid}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="comment_listing")
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, related_name="commentator")
    comment = models.TextField(blank= False)

    def __str__(self):
        return f"{self.comment}"







