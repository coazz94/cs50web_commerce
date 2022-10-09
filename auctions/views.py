from ast import arg
from email import message
from msilib.schema import Error
from pickle import NONE
from subprocess import list2cmdline
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required



from .models import *
from . import forms


def index(request):
    """
        Just the index page that is showing or the listings aviable
    """
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True)
    })


def login_view(request):
    """
        If Get return Login Page
        If Post see if user exists / log him in / redirect to index Page
    """
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


@login_required
def watchlist(request):

    watchlist = Watchlist.objects.filter(user=request.user.id)


    return render(request, "auctions/watchlist.html",{

        "watchlist": watchlist
    })






@login_required
def create_listing(request):
    """
        If Post, get the data from the form and put it in the DB via the Model Listing
        IF error with data return Error Page
    """

    if request.method == "POST":
        form_data = forms.CreateListing(request.POST or None, request.FILES or None)

        if form_data.is_valid():

            title = form_data.cleaned_data["title"]
            description = form_data.cleaned_data["description"]
            price = form_data.cleaned_data["price"]
            img = form_data.cleaned_data["image"]
            print(img)
            category = form_data.cleaned_data["category"]

            listing = Listing(title=title, description=description, price=price, image=img, category=category, active=True, created_by=User.objects.get(id=request.user.id))
            listing.save()

            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/error.html", {
                "message": "Ups something went wrong with creating your listing, please try again"
            })

    else:
        return render(request, "auctions/create.html", {
            "form": forms.CreateListing()
        })


def listing(request, listing_id):

    on_watchlist = True
    item = Listing.objects.get(id=listing_id)
    watchlist = Watchlist.objects.filter(user=request.user.id)

    bid_count =  Bid.objects.filter(listing=listing_id).count()
    highest_bid = Bid.objects.filter(listing=listing_id).order_by("-bid_price").first()


    for items in watchlist:
        if item.title == items.listing.title:
            on_watchlist = False

    if item.created_by.username == request.user.username:
        creator = True
    else:
        creator = False


    return render(request, "auctions/listing.html", {
        "listing": item,
        "watchlist" : on_watchlist, 
        "bid_count" : bid_count, 
        "highest_bid" : highest_bid,
        "creator" : creator

    })




    #später aktiveren
    #try:
    #    return render(request, "auctions/listing.html", {
    #        "listing": item,
    #        "watchlist" : on_watchlist
    #    })
    #except:
    #    return render(request, "auctions/error.html", {
    #        "message": "This item dosent exist"
    #    })


@login_required
def add_watchl(request):
    
    listing_id = request.POST.get("add")

    watchlist = Watchlist()
    watchlist.user = User.objects.get(id = request.user.id)
    watchlist.listing = Listing.objects.get(id = listing_id)
    watchlist.save()
   
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    
@login_required
def remove_watchl(request):

    listing_id = request.POST.get("remove")
    
    Watchlist.objects.filter(user=request.user.id, listing=listing_id).delete()
    
    return HttpResponseRedirect(reverse('listing', kwargs=[listing_id]))


@login_required
def make_bid(request):
    
    try:
        bid_price= float(request.POST["bid_price"])
        listing_id = request.POST.get("make_bid")
        starting_price = float(Listing.objects.get(id = listing_id).price)      
        highest_bid = Bid.objects.filter(listing=listing_id).order_by("-bid_price").first()     

        if not highest_bid:
            highest_bid = 0
        else:
            highest_bid = highest_bid.bid_price   

        if bid_price < highest_bid or bid_price < starting_price:
            raise ValueError
        else:
            listing = Listing.objects.get(id = listing_id)
            user = User.objects.get(id = request.user.id)
            bid = Bid(listing=listing,user= user , bid_price = bid_price)
            bid.save()

        return HttpResponseRedirect(reverse('listing', kwargs={"listing_id":listing_id}))       

    except:
           return render(request, "auctions/error.html", {
             "message": "Ups something went wrong with your bid, make sure that your bid is higher than the current one and the starting price" })
         


    
def end_auction():
    pass