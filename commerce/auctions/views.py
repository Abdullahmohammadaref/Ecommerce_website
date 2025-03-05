from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaultfilters import first
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Category, Listing, Bid, Comment, Watchlist


def index(request):
    if request.user.is_authenticated:
        return render(request,'auctions/index.html',{
            "listings": Listing.objects.all(),
        })
    else:
        return render(request, "auctions/login.html")


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
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/login.html")


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
    if request.user.is_authenticated:
        return render(request,'auctions/categories.html',{
            "categories": Category.objects.all(),
        })
    else:
        return render(request, "auctions/login.html")

def watchlist(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_watchlist = Watchlist.objects.filter(user_id = user_id)
        user_watchlist_listings = [entry.listing for entry in user_watchlist]
        return render(request, "auctions/watchlist.html",{
            "listings": user_watchlist_listings,
        })
    else:
        return render(request, "auctions/login.html")


def create_listing(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["description"]
            price = request.POST["price"]
            picture_url = request.POST["picture_url"]
            category_name = request.POST["category"]

            category, created = Category.objects.get_or_create(name=category_name)

            listing = Listing(
                publisher = request.user,
                title=title,
                picture=picture_url,
                description=description,
                price=price,
                category=Category.objects.get(name=category),
            )
            listing.save()
            return redirect("listing", listing_id=listing.id)
        else:
            return render(request, "auctions/create_listing.html")
    else:
        return render(request, "auctions/login.html")

def listing(request, listing_id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk=listing_id)
        listing_publisher_id = listing.publisher_id
        user_id = request.user.id
        current_listing_in_watchlist = Watchlist.objects.filter(user_id=user_id, listing_id=listing_id).exists()
        listing_bids = Bid.objects.filter(listing_id=listing_id)
        listing_highest_bid = listing_bids.order_by('-bid').first()
        if request.method == "POST":
            form_type = request.POST.get("form_type")
            if form_type == "wishlist":
                current_listing_in_watchlist = Watchlist.objects.filter(user_id=user_id, listing_id=listing_id).exists()
                if current_listing_in_watchlist:
                    Watchlist.objects.get(listing_id=listing_id, user_id=user_id).delete()
                else:
                    current_listing = Watchlist(listing_id=listing_id, user_id=user_id)
                    current_listing.save()

                return redirect("listing", listing_id=listing_id)

            elif form_type == "place_bidding":
                bid = float(request.POST["price"])
                try:
                    if listing.price < bid:
                        listing.price = bid
                        listing.save()
                        current_bid = Bid.objects.create(bidder_id=user_id, listing_id=listing_id, bid=bid)
                        current_bid.save()
                        return redirect("listing", listing_id=listing_id)
                    else:
                        raise ValueError("Bid must be higher than the current price")
                except ValueError as e:
                    messages.error(request, str(e), extra_tags="bid_error")
                    return redirect("listing", listing_id=listing_id)

            elif form_type == "comment":
                comment = request.POST["comment"]
                listing_comment = Comment.objects.create(commentator_id=user_id, listing_id=listing_id, comment=comment)
                listing_comment.save()
                return redirect("listing", listing_id=listing_id)

            elif form_type == "close_listing":
                listing.closed = True
                listing.save()
                return redirect("listing", listing_id=listing_id)


        comments = Comment.objects.filter(listing_id=listing_id)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "current_listing_in_watchlist": current_listing_in_watchlist,
            "current_user_id": user_id,
            "listing_publisher_id": listing_publisher_id,
            "comments": comments,
            "listing_highest_bid": listing_highest_bid,
            })
    else:
        return render(request, "auctions/login.html")


def category_listings(request, category_id):
    if request.user.is_authenticated:
        category= Category.objects.get(pk=category_id)
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/category_listings.html",{
            "listings": listings,
            "category": category
        })
    else:
        return render(request, "auctions/login.html")