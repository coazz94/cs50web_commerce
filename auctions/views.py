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


def listing(request, listing_id):

    """
        try:
            display the listing page with all the needed paramters
        except:
            return an error Page
    """
    try:

        # get the item and the watchlist of the user
        item = Listing.objects.get(id=listing_id)
        watchlist = Watchlist.objects.filter(user=request.user.id)
        on_watchlist = False

        # get the bid count and highest_bid of the listing
        bid_count =  Bid.objects.filter(listing=listing_id).count()
        highest_bid = Bid.objects.filter(listing=listing_id).order_by("-bid_price").first()

        # check if the item is already on the watchlist
        for items in watchlist:
            if item.title == items.listing.title:
                on_watchlist = True

        # check if the user has created the listing (to gain acces to end_auction)
        if item.created_by.username == request.user.username:
            creator = True
        else:
            creator = False

        # get all the comments for the listing
        comments = Comments.objects.filter(listing=listing_id)

        # render the Page with the infos
        return render(request, "auctions/listing.html", {
            "listing": item,
            "watchlist" : on_watchlist, 
            "bid_count" : bid_count, 
            "highest_bid" : highest_bid,
            "creator" : creator,
            "comments" : comments
        })


    except:
        return render(request, "auctions/error.html", {
            "message": "This item dosent exist"
        })
        

@login_required
def watchlist(request):
    """
       Render a Watchlistpage that shows the Users watchlist
    """

    watchlist = Watchlist.objects.filter(user=request.user.id)

    return render(request, "auctions/watchlist.html",{
        "watchlist": watchlist,
    })


@login_required
def create_listing(request):
    """
        If Post, get the data from the form and put it in the DB via the Model Listing
        If error with data return Error Page
    """

    if request.method == "POST":

        # get the form data
        form_data = forms.CreateListing(request.POST or None, request.FILES or None)

        # if the data is valid than proceed
        if form_data.is_valid():

            #img = form_data.cleaned_data["image"] // manual Image Upload deactivated
            title = form_data.cleaned_data["title"]
            description = form_data.cleaned_data["description"]
            price = form_data.cleaned_data["price"]
            category = form_data.cleaned_data["category"]
            img_url = form_data.cleaned_data["img_url"]
            
            # make a new Listing object, with the parameters from above
            listing = Listing(title=title, description=description, price=price, image_url=img_url, category=category, active=True, created_by=User.objects.get(id=request.user.id))
            listing.save()

            # return to the index Page
            return HttpResponseRedirect(reverse("index"))

        else:
        
            # Render an Error Page if the form was not valid
            return render(request, "auctions/error.html", {
                "message": "Ups something went wrong with creating your listing, please try again"
            })

    else:
        # if get than render the page for creating a listing
        return render(request, "auctions/create.html", {
            "form": forms.CreateListing()
        })


@login_required
def add_watchl(request):
    """
        add a listing to the users watchlist
    """

    # get the listing id from the Post form
    listing_id = request.POST.get("add")

    # new instance of the watchlist, and add the user and the listing to it
    watchlist = Watchlist()
    watchlist.user = User.objects.get(id = request.user.id)
    watchlist.listing = Listing.objects.get(id = listing_id)
    watchlist.save()

    # refresh the listing Page
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    

@login_required
def remove_watchl(request):
    """
        remove item from the listing Page
    """

    # get the listing via the id proviedes by the form 
    listing_id = request.POST.get("remove")
    
    # filter the listing via the id and the user from the watchlist
    Watchlist.objects.filter(user=request.user.id, listing=listing_id).delete()
    
    # refresh the listin page again
    return HttpResponseRedirect(reverse('listing', kwargs={"listing_id":listing_id}))


@login_required
def make_bid(request):

    """
        a function to make the bid for the item
        we have to check some dependecies and than be able to save the bid
    """
    try:

        # get the bid price provided and the listing
        bid_price= float(request.POST["bid_price"])
        listing_id = request.POST.get("make_bid")

        # get the starting price and the highest bid ever
        starting_price = float(Listing.objects.get(id = listing_id).price)      
        highest_bid = Bid.objects.filter(listing=listing_id).order_by("-bid_price").first()    

        # check if a bid was ever made, when not than ste the price to 0 else set it to the higest bid price ever made
        if not highest_bid:
            highest_bid = 0
        else:
            highest_bid = highest_bid.bid_price   

        # if the bid price is bigger than the startingprice/ highest bid 
        if bid_price > highest_bid and bid_price > starting_price:

            #Update the highest bid value
            listing = Listing.objects.filter(id = listing_id)
            listing.update(highest_bid=bid_price)

            # save the bid
            listing = Listing.objects.get(id = listing_id)
            user = User.objects.get(id = request.user.id)
            bid = Bid(listing = listing,user = user , bid_price = bid_price)
            bid.save()

        else:
            return render(request, "auctions/error.html", {
                "message": "Ups something went wrong with your bid, make sure that your bid is higher than the current one and the starting price" })

        # return the listing Page
        return HttpResponseRedirect(reverse('listing', kwargs={"listing_id":listing_id}))       

    except:

        # if something went wrong with the post arguments return a error Page
        return render(request, "auctions/error.html", {
          "message": "Ups something went wrong with your bid, make sure that your bid is higher than the current one and the starting price, dont use comma only dot(example: 5.55)" })


@login_required 
def end_auction(request):
    """
        end the auction if the user is logged in who made the article
    """
    
    # get the listingid provideds from the post form
    listing_id = request.POST["end_auction"]

    # get the highest bid ever
    highest_bid = Bid.objects.filter(listing=listing_id).order_by("-bid_price").first()

    # update the listing ( change status to not active, and provide info about the winner of the auction)
    listing = Listing.objects.filter(id=listing_id)    
    listing.update(active=False)
    listing.update(winner=highest_bid.user)

    # refresh the listing page
    return HttpResponseRedirect(reverse('listing', kwargs={"listing_id":listing_id}))
    
@login_required 
def comment(request):
    """
        comment on the listing that was provides by the Post.get function
        make a new comment and save it, return to the same item 
    """

    # get the comment and listing.id
    comment = request.POST.get("comment")
    listing_id = request.POST.get("add_comment")

    # get the listing and the user from their ids
    listing = Listing.objects.get(id = listing_id)
    user = User.objects.get(id = request.user.id)

    # make a new instance of the comment model and sav it
    new_com = Comments(listing=listing, user=user, comment = comment)
    new_com.save()


    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id" : listing_id}))


def categories(request):
    """
        if mehtod == GET than return the view Page of the categoires
        if POST than get the category from the Post.get, and render the index page with a filter 
    """
    
    if request.method == "POST":
        
        category = request.POST.get("category")

        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(category=category)
        })

    else:
        return render(request, "auctions/categories.html", {
            "categories" : forms.CATEGORIES
        })