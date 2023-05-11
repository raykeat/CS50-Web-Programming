from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionsListings(models.Model):
    title = models.CharField(max_length=64,default="title")
    description = models.CharField(max_length=300,default = "description")
    startingbid = models.IntegerField(default="startingbid")
    imageurl = models.CharField(max_length=128,default="imageurl")
    category = models.CharField(max_length=64,default="category")
    user = models.ForeignKey(User,related_name="auctionproduct",on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)
    highest_bidder = models.CharField(max_length=64,default="None")
    highest_bid = models.IntegerField(max_length=64,default=0)
    noofbids = models.IntegerField(max_length=64,default=0)
    addedtowatchlist = models.BooleanField(default=False)
    watchlist_adder = models.CharField(max_length=64,default = "None")

class Bid(models.Model):
    bidproduct = models.ForeignKey(AuctionsListings,on_delete=models.CASCADE,related_name="bidobject")
    bidprice = models.IntegerField(max_length=10,default=0)
    user = models.ForeignKey(User,related_name="productbid",on_delete=models.CASCADE)

class CommentsAuctions(models.Model):
    comments = models.CharField(max_length=300,default="comments")
    product = models.ManyToManyField(AuctionsListings,related_name="CommentsAuctions")


