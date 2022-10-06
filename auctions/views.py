from pickle import NONE
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from . import forms


def index(request):
    """
        Just the index page that is showing or the listings aviable
    """
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

def watchlist(request, user_id):

    info = User.objects.get(id=user_id)

    return render(request, "auctions/watchlist.html",{

        "user_items": info.listing.all()
    })


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
            category = form_data.cleaned_data["category"]

            listing = Listing(title=title, description=description, price=price, image=img, category=category)
            listing.save()

        else:
            return render(request, "auctions/error.html", {
                "message": "Ups something went wrong with creating your listing, please try again"
            })

    else:
        return render(request, "auctions/create.html", {
            "form": forms.CreateListing()
        })


def listing(request):

    id = request.GET["subjectID"]


    try:
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(id=id)
        })
    except:
        return render(request, "auctions/error.html", {
            "message": "This item dosent exist"
        })



def add_watchl(request, listing_id):
    
    item = Listing.objects.get(id=listing_id)

    """
        Add hier einfach zum Listing
    """

    print(item.title)

    