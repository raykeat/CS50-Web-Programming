from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, AuctionsListings, Bid, CommentsAuctions

def index(request):
    #getting all the product listings stored in the AuctionsListings Model
    allproductlistings = AuctionsListings.objects.all()
    return render(request,"auctions/index.html",{
        "productlistings":allproductlistings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

#decorator that ensures user is authenticated and logged in before they can access the view
@login_required
def createnewlisting(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        startingbid = request.POST['startingbid']
        imageurl = request.POST['imageurl']
        category = request.POST['category']

        #creating an instance of the AuctionsListings Model with the details submitted in the form
        newlisting = AuctionsListings(title=title,description=description,startingbid=startingbid,imageurl=imageurl,category=category)
        newlisting.user = request.user
        newlisting.save()

        #getting all the product listings stored in the AuctionsListings Model
        allproductlistings = AuctionsListings.objects.all()
        return render(request,"auctions/index.html",{
            "productlistings":allproductlistings
        })

    # if request method is GET
    else:
        return render(request,"auctions/newlisting.html")
    
#directs user to newpage only for that specific listing
def specificlisting(request,id):
    #getting details of specific listing
    listing = AuctionsListings.objects.get(pk=id)
    personwholisted = listing.user.username
    auction_ended = listing.is_closed

    bidder = listing.highest_bidder
    highestbid = listing.highest_bid
    if auction_ended is True:
        message = f"Auction for {listing.title} has closed and {listing.title} is sold to {bidder} at ${highestbid}"
    else:
        message = f"{listing.noofbids} bid(s) so far."

    #showing comments
    products = CommentsAuctions.objects.filter(product=listing)
    comments = [comment.comments for comment in products]

    #checking if listing is in watchlist
    try:
        added_to_watchlist = True if listing in request.user.watchlist_objects.all() else False
    except:
        added_to_watchlist = False
    
    return render(request,"auctions/specificlisting.html",{
        "listing":listing,
        "personwholisted":personwholisted,
        "message":message,
        "auction_ended":auction_ended,
        "currentprice":highestbid,
        "comments":comments,
        "added_to_watchlist":added_to_watchlist
    })

#allows user to bid for an auction product
@login_required
def bid(request):
    
        bidprice = int(request.POST['bidprice'])
        bidproducttitle = request.POST['listing']
        bidproduct = AuctionsListings.objects.get(title=bidproducttitle)

        #getting highest bid thus far
        listofbids = Bid.objects.filter(bidproduct=bidproduct)
        if listofbids:
            currentprice = max([bid.bidprice for bid in listofbids])
        else:
            currentprice = bidproduct.startingbid

        #showing list of comments for a product
        try:
            object = CommentsAuctions.objects.get(product=bidproduct)
            if object.commentcount == 1:
                comments = [object.comments]
            else:
                comments = object.comments.split(", ")
        except:
            comments = []

        #if bid price is less than starting bid
        if bidprice<int(bidproduct.startingbid):
            return render(request,"auctions/specificlisting.html",{
                "message":f"Bid price must be at least ${bidproduct.startingbid}. Please enter higher bid",
                "listing":bidproduct,
                "currentprice":currentprice,
                "comments":comments
            })
        
        #if bid price is less than other bids done by users
        allbids = Bid.objects.filter(bidproduct=bidproduct)
        listofprices = [bid.bidprice for bid in allbids]
        for price in listofprices:
            if float(bidprice) <= float(price):
                return render(request,"auctions/specificlisting.html",{
                "message":f"Bid price must be higher than ${price}. Please enter higher bid",
                "listing":bidproduct,
                "currentprice":currentprice,
                "comments":comments
            })
        
        currentbid = Bid(bidproduct=bidproduct,bidprice=bidprice,user=request.user)
        currentbid.save()
        bidproduct.highest_bid = bidprice
        listofbids = [bid for bid in Bid.objects.filter(bidproduct = bidproduct)]
        noofbids=len(listofbids)
        bidproduct.noofbids=noofbids
        bidproduct.save()
        return render(request,"auctions/specificlisting.html",{
            "message":f"{noofbids} bid(s) so far. Your bid of ${bidprice} is the current bid",
            "listing":bidproduct,
            "currentprice":bidprice,
            "comments":comments
        })

@login_required
def closeauction(request):
    producttitle = request.POST['listing']
    product = AuctionsListings.objects.get(title=producttitle)
    listofbids = Bid.objects.filter(bidproduct = product)
    highestbid=0

    #getting the highest bid and its bidder
    for bid in listofbids:
        if bid.bidprice>highestbid:
            highestbid = bid.bidprice
            highestbidder = bid.user.username

    producttitle = product.title
    #updating that Auctioning for this product is closed in AuctionsListings Model
    product.is_closed = True
    auction_ended = True
    #updating the highest bid and bidder for a product in AuctionsListings Model
    product.highest_bidder = highestbidder
    product.highest_bid = highestbid
    product.save()

    #checking if listing is in watchlist
    added_to_watchlist = True if product in request.user.watchlist_objects.all() else False

    #showing list of comments for a product
    try:
        object = CommentsAuctions.objects.get(product=product)
        if object.commentcount == 1:
            comments = [object.comments]
        else:
            comments = object.comments.split(", ")
    except:
        comments = []

    #generating message about auction bids for that product
    if product.is_closed:
        message = f"Auction for {producttitle} has closed and {producttitle} is sold to {product.highest_bidder} at ${product.highest_bid}"
    else:
        message = f"{product.noofbids} bid(s) so far."

    return render(request,"auctions/specificlisting.html",{
        "message":message,
        "auction_ended":auction_ended,
        "listing":product,
        "comments":comments,
        "added_to_watchlist":added_to_watchlist
    })

@login_required
def addcomment(request):
    comment = request.POST['comment']
    producttitle = request.POST['listing']
    product = AuctionsListings.objects.get(title=producttitle)
    
    #check if CommentsAuctions object for this product has been created,
    #otherwise initialize an instance of CommentsAuctions class
    commentobject = CommentsAuctions.objects.filter(product=product).first()
    if commentobject:
        updatedcomments = commentobject.comments + f", {comment}"
        commentobject.comments = updatedcomments
        commentobject.commentcount+=1
        commentobject.save()
    
    else:
        CommentsAuctions.objects.create(product=product,comments=comment,commentcount=1)
    

    #showing list of comments for a product
    object = CommentsAuctions.objects.get(product=product)
    if object.commentcount == 1:
        comments = [object.comments]
    else:
        comments = object.comments.split(", ")

    #generating message about auction bids for that product
    if product.is_closed:
        message = f"Auction for {producttitle} has closed and {producttitle} is sold to {product.highest_bidder} at ${product.highest_bid}"
    else:
        message = f"{product.noofbids} bid(s) so far."
    return render(request,"auctions/specificlisting.html",{
        "comments":comments,
        "listing":product,
        "message":message
    })

@login_required
def addwatchlist(request):
    if request.method == "POST":
        producttitle = request.POST['listing']
        product = AuctionsListings.objects.get(title=producttitle)
        request.user.watchlist_objects.add(product)
        request.user.save()

        #showing list of comments for a product
        try:
            object = CommentsAuctions.objects.get(product=product)
            if object.commentcount == 1:
                comments = [object.comments]
            else:
                comments = object.comments.split(", ")
        except:
            comments = []


        #checking if listing is in watchlist
        added_to_watchlist = True if product in request.user.watchlist_objects.all() else False

        #generating message about auction bids for that product
        if product.is_closed:
            message = f"Auction for {producttitle} has closed and {producttitle} is sold to ${product.highest_bidder} at {product.highest_bid}"
        else:
            message = f"{product.noofbids} bid(s) so far."

        return render(request,"auctions/specificlisting.html",{
            "comments":comments,
            "listing":product,
            "message":message,
            "added_to_watchlist":added_to_watchlist
        })

    #if request.method =="GET"
    else:
        listofproducts = [product for product in request.user.watchlist_objects.all()]
        return render(request,"auctions/watchlist.html",{
            "listofproducts":listofproducts
        })

@login_required
def removewatchlist(request):
    if request.method == "POST":
        producttitle = request.POST['listing']
        product = AuctionsListings.objects.get(title=producttitle)
        request.user.watchlist_objects.remove(product)
        request.user.save()

        #showing list of comments for a product
        try:
            object = CommentsAuctions.objects.get(product=product)
            if object.commentcount == 1:
                comments = [object.comments]
            else:
                comments = object.comments.split(", ")
        except:
            comments = []

        #checking if listing is in watchlist
        added_to_watchlist = True if product in request.user.watchlist_objects.all() else False

        #generating message about auction bids for that product
        if product.is_closed:
            message = f"Auction for {producttitle} has closed and {producttitle} is sold to ${product.highest_bidder} at {product.highest_bid}"
        else:
            message = f"{product.noofbids} bid(s) so far."

        return render(request,"auctions/specificlisting.html",{
            "comments":comments,
            "listing":product,
            "message":message,
            "added_to_watchlist":added_to_watchlist
        })

    
#getting all the different categories
def categorieslist(request):

    #values_list() is used to retrieve only the category field values from the model instances, 
    #and flat=True is used to flatten the resulting list into a 1-dimensional list of values.
    categories = list(AuctionsListings.objects.values_list('category', flat=True).distinct())
    return render(request,"auctions/categories.html",{
        "categories":categories,
    })
    
#displaying all products for a certain category
def category(request,category):
    listofproducts = list(AuctionsListings.objects.filter(category=category))
    return render(request,"auctions/specificcategory.html",{
        "listofproducts":listofproducts,
        "category":category
    })


