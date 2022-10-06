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


def watchlist(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "auctions/watchlist.html")


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

    if request.method == "POST":
        pass

        """
            Watchlist hinzufügen muss also ein template machen unten bei else 
            Button = add to watch list = soll in ein neues Model adden 
            Button Bid = check das der Preis größer ist, wenn nicht zeige text an mit django if
            wenn schon aktualisieren den Bid auch ein model 
            
            speichere irgednwo auch welcher user welches bid gemacht hat und schaue ob der user dieses Bid gemacht hat 
            wenn ja kann er es dekativeiren 
            wenn nein dann nicht ( jinja if )
        
            im auction model noch eine zeile mit id from user der das geamcht hat ? 
            user id dann auch vergeben ! und linken 
            
        """

    else:
        try:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(id=id)
            })
        except:
            return render(request, "auctions/error.html", {
                "message": "This item dosent exist"
            })
