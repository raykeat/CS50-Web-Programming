from django.contrib import admin
from .models import User, AuctionsListings, Bid, CommentsAuctions
# Register your models here.

#registers the models in admin app to allow us to use the admin app to manipulate these models/tables
admin.site.register(User)
admin.site.register(AuctionsListings)
admin.site.register(Bid)
admin.site.register(CommentsAuctions)