from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from . import forms


def index(request):

    #dodji to podataka iz baze i izbaci ih u neku listu ili tkao i onda ih prebaci samo u index html ( mozda bootstrap da izgldea lijepse)
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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


def watchlist(request):   
    if request.method == "POST":
        pass
    else:
        return render(request, "auctions/watchlist.html")



def create_listing(request):
    
    if request.method == "POST":
        form_data = forms.CreateListing(request.POST)

        if form_data.is_valid():


            title = form_data.cleaned_data["title"]
            description = form_data.cleaned_data["description"]
            price = form_data.cleaned_data["price"]
            url = form_data.cleaned_data["url"]
            
            listing = Listing(name=title, description=description, price=price, url=url)
            listing.save()

        
        #else:
        return render(request, "auctions/create.html", {
            "form" : forms.CreateListing()
        })

    else:
        return render(request, "auctions/create.html", {
            "form" : forms.CreateListing()
        })