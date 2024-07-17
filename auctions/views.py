from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing, Comment, Bid

def index(request):
    listings = Listing.objects.all()
    countOfWatchlistItems=0
    if request.user.is_authenticated:
        items = request.user.watchlistitems.all()
        countOfWatchlistItems = items.count()
    return render(request, "auctions/index.html", {
        "listings": listings ,
        "count": countOfWatchlistItems
    })

def createNewListing(request):
    listings = request.user.watchlistitems.all()
    countOfWatchlistItems = listings.count()
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "allcategories": categories,
            "count":countOfWatchlistItems
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["url"]
        price = request.POST["price"]
        category = request.POST["category"]
        categoryname = Category.objects.get(Category=category)
        user = request.user
        bid = Bid(bidValue=float(price), user=user)
        bid.save()
        l = Listing(title=title, description=description, imageUrl=imageurl, startingPrice= price, currentPrice=bid, category=categoryname, owner=user)
        l.save()
        return HttpResponseRedirect(reverse(index))

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

def categories(request):
    categories = Category.objects.all()
    countOfWatchlistItems=0
    if request.user.is_authenticated:
        items = request.user.watchlistitems.all()
        countOfWatchlistItems = items.count()
    return render(request, "auctions/categories.html", {
        "categories": categories ,
        "count": countOfWatchlistItems
    })

def categoryPage(request, category):
    categoryname = Category.objects.get(Category=category)
    listings = Listing.objects.filter(category=categoryname)
    countOfWatchlistItems=0
    if request.user.is_authenticated:
        items = request.user.watchlistitems.all()
        countOfWatchlistItems = items.count()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "count": countOfWatchlistItems
    })

def listing(request, id):
    listing = Listing.objects.get(pk=id)
    IsInWatchlist = request.user in listing.watchlist.all()
    allComments = Comment.objects.filter(listing=listing)
    isOwner = (request.user == listing.owner)
    countOfWatchlistItems=0
    if request.user.is_authenticated:
        items = request.user.watchlistitems.all()
        countOfWatchlistItems = items.count()
    return render(request, "auctions/listing.html",{
        "listing":listing,
        "IsInWatchlist": IsInWatchlist,
        "comments": allComments,
        "isOwner": isOwner,
        "count": countOfWatchlistItems
    })

def additem(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def removeitem(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlist(request):
    user = request.user
    listings = user.watchlistitems.all()
    countOfWatchlistItems = listings.count()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "count": countOfWatchlistItems
    })

def addcomment(request, id):
    user = request.user
    message = request.POST["comment"]
    listing = Listing.objects.get(pk = id)
    comment = Comment(user=user, message=message, listing=listing)
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addbid(request, id):
    newbid = request.POST["bid"]
    listing = Listing.objects.get(pk=id)
    IsInWatchlist = request.user in listing.watchlist.all()
    isOwner = request.user == listing.owner
    listings = request.user.watchlistitems.all()
    countOfWatchlistItems = listings.count()
    allComments = Comment.objects.filter(listing=listing)
    if float(newbid) > float(listing.currentPrice.bidValue):
        updateBid = Bid(user=request.user, bidValue=float(newbid))
        updateBid.save()
        listing.currentPrice = updateBid
        listing.save()
        BidIsLarger = True
        message = "Bid succesful!"
    else:
        BidIsLarger = False
        message = "Bid unsuccessful!"
    return render(request, "auctions/listing.html", {
        "count": countOfWatchlistItems,
        "listing": listing,
        "BidIslarger": BidIsLarger,
        "message": message,
        "IsInWatchlist": IsInWatchlist,
        "isOwner": isOwner,
        "comments": allComments,
    })

def closelisting(request, id):
    listing = Listing.objects.get(pk=id)
    listings = request.user.watchlistitems.all()
    countOfWatchlistItems = listings.count()
    listing.isActive = False
    listing.save()
    IsInWatchlist = request.user in listing.watchlist.all()
    isOwner = (request.user == listing.owner)
    allComments = Comment.objects.filter(listing=listing)
    return render(request, "auctions/listing.html",{
        "listing":listing,
        "count": countOfWatchlistItems,
        "IsInWatchlist": IsInWatchlist,
        "comments": allComments,
        "isOwner": isOwner,
        "BidIslarger": True,
        "message": "Your listing is closed."
    })
