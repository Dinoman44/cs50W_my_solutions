from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import AuctionListing, User, Bid, Comment, Watchlist

categories = ["Books", "Stationary", "Clothing", "Household", "Sports", "Electronics", "Toys", "Decorations", "Assorted"]
def index(request):
    listings_data = AuctionListing.objects.filter(is_active=True).order_by("-sell_date")
    listings = []
    for listing in listings_data:
        listings.append([listing.item_name, listing.item_description, listing.seller.username, listing.current_price, listing.sell_date, listing.listing_id, listing.img.name[9:]])
    return render(request, "auctions/index.html", {
        "listings": listings,
        "categories": categories,
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
            return redirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    # logout the user
    logout(request)
    return redirect(reverse("index"))


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
        return redirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def add_listing(request):
    # if the page is GETed
    if request.method == "GET":
        return render(request, "auctions/add_listing.html", {
            "categories": categories
            })

    # if a new listing is being added
    else:
        # get the listing details and add them to the database
        item_name = request.POST["item_name"]
        item_descr = request.POST["item_descr"]
        base_price = request.POST["base_price"]
        category = request.POST["category"]
        img = request.FILES["img"]
        listing = AuctionListing(seller=request.user, item_name=item_name, item_description=item_descr, img=img, category=category, current_price=base_price, sell_date=timezone.now(), is_active=True)
        listing.save()
        return redirect(reverse("index"))


@login_required(login_url="/login")
def see_listing(request, listing_id):
    # if the user is bidding on the object
    if request.method == "POST":
        # get the user's bid
        user_bid = float(request.POST.get("bid"))
        listing_id = request.POST.get("listing_id")
        # get the listing that is being bid upon
        listing = AuctionListing.objects.filter(listing_id=listing_id).first()
        # update its currrent bid, and add the bid to the database
        if listing.current_price < user_bid:
            new_bid = Bid(bidding_on=listing, bid_amt=user_bid, bid_by=request.user)
            new_bid.save()
            listing.current_price = user_bid
            listing.save()
        return redirect(reverse("index"))

    # get the listing the user wants to see, and send it to be displayed
    listing = AuctionListing.objects.filter(listing_id=listing_id).first()
    x = Watchlist.objects.filter(watched=listing_id, watcher=request.user, still_watching=True)
    if len(x):
        watching = True
    else:
        watching = False
    if not listing.is_active:
        highest_bid = Bid.objects.filter(bidding_on=listing, bid_amt=listing.current_price).first()
        if highest_bid:
            highest_bidder = highest_bid.bid_by
        else:
            highest_bidder = "nobody"
    else:
        highest_bidder = False
    comments = Comment.objects.filter(commented_on=listing)
    return render(request, "auctions/see_listing.html", {
        "listing": listing,
        "img": listing.img.name[9:],
        "watching": watching,
        "winner": highest_bidder,
        "comments": comments
    })


@login_required(login_url="/login")
def user_listings(request):
    # get the user's listings and display them
    listings_data = AuctionListing.objects.filter(seller=request.user).order_by("-sell_date")
    listings = []
    for listing in listings_data:
        listings.append([listing.item_name, listing.item_description, listing.seller.username, listing.current_price, listing.sell_date, listing.listing_id, listing.img.name[9:], listing.is_active])
    return render(request, "auctions/user_listings.html", {
        "listings": listings
    })


@login_required(login_url="/login")
def close_auction(request, listing_id):
    # close the auction(only can be done by the user)
    listing = AuctionListing.objects.filter(listing_id=listing_id).first()
    # if the seller and the user closing the auction are the same
    if listing.seller == request.user:
        # make listing inactive
        listing.is_active = False
        listing.save()
        return redirect(reverse("index"))

    # if a different user (somehow) requested this
    else:
        return redirect(reverse("index"))


def check_category(request, category):
    listings_data = AuctionListing.objects.filter(is_active=True, category=category).order_by("-sell_date")
    listings = []
    for listing in listings_data:
        listings.append([listing.item_name, listing.item_description, listing.seller.username, listing.current_price, listing.sell_date, listing.listing_id, listing.img.name[9:]])
    return render(request, "auctions/categoryfilter.html", {
        "listings": listings,
        "categories": categories,
        "category": category
    })


@login_required(login_url="/login")
def watchlist(request):
    watched_items = []
    # get the user's watchlisted items
    for i in Watchlist.objects.filter(watcher=request.user, still_watching=True).order_by("-id"):
        watched_items.append(i.watched)
    listings = []
    for listing in watched_items:
        listings.append([listing.item_name, listing.item_description, listing.seller.username, listing.current_price, listing.sell_date, listing.listing_id, listing.img.name[9:]])
    return render(request, "auctions/watchlist.html", {
        "watched_items": listings
    })


@login_required(login_url="/login")
def add2watchlist(request, listing_id):
    # get the listing id
    listing = AuctionListing.objects.filter(listing_id=listing_id).first()
    x = Watchlist.objects.filter(watcher=request.user, watched=listing)
    # add item to watchlist
    if len(x) == 1 and not x.first().still_watching:
        x = x.first()
        x.still_watching = True
        x.save()
    elif len(x) == 0:
        watchlistitem = Watchlist(watcher=request.user, watched=listing, still_watching=True)
        watchlistitem.save()
    return redirect(reverse("index"))


@login_required(login_url="/login")
def removefromwatchlist(request, listing_id):
    # get the listing
    listing = AuctionListing.objects.filter(listing_id=listing_id).first()
    x = Watchlist.objects.filter(watcher=request.user, watched=listing)
    # check if the user has already added item to watchlist
    if len(x) == 1:
        x = x.first()
        # if it is still on the watchlist
        if x.still_watching:
            x.still_watching = False
            x.save()
    return redirect(reverse("index"))


@login_required
def comment(request, listing_id):
    comment_txt = request.POST.get("comment")
    listing = AuctionListing.objects.filter(listing_id=listing_id).first()
    comment = Comment(commented_on=listing, commented_when=timezone.now(), commenter=request.user, comment_txt=comment_txt)
    comment.save()
    return redirect(reverse("see_listing", args=[listing_id]))







