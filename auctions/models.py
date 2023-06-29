from django.contrib.auth.models import AbstractUser
from django.db import models


class AuctionsListings(models.Model):
    title = models.CharField(max_length=64,default="title")
    description = models.CharField(max_length=300,default = "description")
    startingbid = models.IntegerField(default="startingbid")
    imageurl = models.CharField(max_length=128,default="imageurl")
    category = models.CharField(max_length=64,default="category")
    user = models.ForeignKey('User',related_name="auctionproduct",on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)
    highest_bidder = models.CharField(max_length=64,default="None")
    highest_bid = models.IntegerField(max_length=64,default=0)
    noofbids = models.IntegerField(max_length=64,default=0)

class User(AbstractUser):
    watchlist_objects = models.ManyToManyField(AuctionsListings, related_name="watchlist_users", default=None)
    

class Bid(models.Model):
    bidproduct = models.ForeignKey(AuctionsListings,on_delete=models.CASCADE,related_name="bidobject")
    bidprice = models.IntegerField(max_length=10,default=0)
    user = models.ForeignKey(User,related_name="productbid",on_delete=models.CASCADE)

class CommentsAuctions(models.Model):
    comments = models.CharField(max_length=700,default="comments")
    product = models.ForeignKey(AuctionsListings,related_name="CommentsAuctions",on_delete=models.CASCADE)
    commentcount = models.IntegerField(default=1)


